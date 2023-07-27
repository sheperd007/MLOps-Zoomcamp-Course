import mlflow.tensorflow
from tqdm import tqdm
import cv2
from tensorflow.keras.applications import ResNet50
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.optimizers import Adam
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization, AveragePooling2D, GlobalAveragePooling2D
from keras_preprocessing.image import ImageDataGenerator
import logging
import pickle
import os
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from prefect import flow, task
import requests
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
DB_POSTGRES: str = os.getenv('DB_POSTGRES')
mlflow.set_tracking_uri(DB_POSTGRES)
mlflow.set_experimenct('ResNet-Covid19')

logger = logging.getLogger("MLopz Zoomcamp.py")
logging.basicConfig(level=logging.INFO)
logger.info("Setting dataset Location!")
import os


@task(retries=3, retry_delay_seconds=1, log_prints=True)
def read_data():
    try:
    for dirname, _, filenames in os.walk('./app/data'):
        for filename in filenames:
            os.path.join(dirname, filename)
    except:
        logger.exception("Something goes wrong when reading Dataset")
    logger.info("Make data ready!")

    disease_types = ['COVID', 'non-COVID']

    train_dir = data_dir = './data'

    train_data = []

    for index, sp in enumerate(disease_types):
        for file in os.listdir(os.path.join(train_dir, sp)):
            train_data.append([sp + "/" + file, index, sp])

    train = pd.DataFrame(train_data, columns = ['File', 'ID','Disease Type'])
    train.head()

    IMAGE_SIZE = 150
    def read_image(filepath):
        return cv2.imread(os.path.join(data_dir, filepath))
    def resize_image(image, image_size):
        return cv2.resize(image.copy(), image_size, interpolation=cv2.INTER_AREA)

    X_train = np.zeros((train.shape[0], IMAGE_SIZE, IMAGE_SIZE, 3))
    for i, file in tqdm(enumerate(train['File'].values)):
        image = read_image(file)
        if image is not None:
            X_train[i] = resize_image(image, (IMAGE_SIZE, IMAGE_SIZE))
    X_Train = X_train / 255.

    logger.info("Show Training Dataset Size! = {}".format(X_Train.shape))
    logger.info("Training ResNet Model!")


BATCH_SIZE = 64
EPOCHS = 50
SIZE=150
N_ch=3


def build_resnet50():
    resnet50 = ResNet50(include_top=False)

    input = Input(shape=(SIZE, SIZE, N_ch))
    x = Conv2D(3, (3, 3), padding='same')(input)

    x = resnet50(x)

    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)

    # multi output
    output = Dense(2,activation = 'softmax', name='root')(x)


    # model
    model = Model(input,output)

    optimizer = Adam(lr=0.003, beta_1=0.9, beta_2=0.999, epsilon=0.1, decay=0.0)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    model.summary()

    return model
@task(log_prints=True)
def train_model(X_train,Y_train,BATCH_SIZE,EPOCHS):
    model = build_resnet50()
    annealer = ReduceLROnPlateau(monitor='val_accuracy', factor=0.70, patience=5, verbose=1, min_lr=1e-4)
    checkpoint = ModelCheckpoint('ResNet50_Model.hdf5', verbose=1, save_best_only=True,monitor='val_accuracy')
    datagen = ImageDataGenerator(rotation_range=360,
                                 width_shift_range=0.2,
                                 height_shift_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True,
                                 vertical_flip=True)

    datagen.fit(X_train)
    mlflow.keras.autolog(registered_model_name='ResNet-Model')
    history = model.fit(datagen.flow(X_train, Y_train, batch_size=BATCH_SIZE),
                        steps_per_epoch=X_train.shape[0] // BATCH_SIZE,
                        epochs=EPOCHS,
                        verbose=1,
                        callbacks=[annealer, checkpoint],
                        validation_data=(X_val, Y_val))
    requests.post(f'{os.getenv("EVIDENTLY")}/iterate/covid',json = [history])
@flow
def main_fun(X_train,Y_train,BATCH_SIZE,EPOCHS):
    read_data()
    train_model(X_train,Y_train,BATCH_SIZE,EPOCHS)

if __name__ == "__main__":
    main_fun(X_train,Y_train,BATCH_SIZE,EPOCHS)
with open('./history.bin','wb') as f_out:
    pickle.dump(history,f_out)
mlflow.log_artifact(local_path='./history.bin',artifact_path = 'model_history/')
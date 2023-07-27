import mlflow
from fastapi import APIRouter, Depends


DB_POSTGRES: str = os.getenv('DB_POSTGRES')
mlflow.set_tracking_uri(DB_POSTGRES)
from mlflow.tracking import MlflowClient
client = MlflowClient(tracking_uri=DB_POSTGRES)

runs = client.search_runs(name='ResNet-Covid19')
run_id = run.info.run_id
model_uri = f"runs:/{run_id}/model"
model = mlflow.keras.load_model(model_uri)
router = APIRouter()


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image
@router.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    prediction = model.predict(image)
    return prediction

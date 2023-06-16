#!/usr/bin/env python
# coding: utf-8

# In[1]:


#get_ipython().system('pip freeze | grep scikit-learn')


# In[10]:


import pickle
import pandas as pd
import numpy as np
import sys

# In[4]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[15]:


categorical = ['PULocationID', 'DOLocationID']
year = sys.argv[1] #2022
month = sys.argv[2] #2
def read_data(filename):
    df = pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[16]:


df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')


# In[8]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# In[19]:

np.mean(y_pred)
# In[ ]:





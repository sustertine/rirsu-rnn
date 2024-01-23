import pickle

import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile
# from keras.src.saving.saving_lib import load_model
from keras.models import load_model
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dataprocessing import DataProcessor
from instance import AirQualityData, AirQualityDataList
from io import StringIO

app = FastAPI()

dataProcessor = DataProcessor()
model = load_model('objects/air-quality-gru.h5', compile=False)
with open('objects/target-std-scaler.pkl', 'rb') as file:
    std = pickle.load(file)
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')

@app.post("/predict")
async def predict_csv(file: UploadFile = File(...)):
    stringio = StringIO(str(await file.read(), 'utf-8'))

    df = pd.read_csv(stringio)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    df.set_index('Date', inplace=True)

    X = dataProcessor.processDf(df)
    X_combined = np.array([window.to_numpy() for window in X])
    preds = model.predict(X_combined)
    preds = std.inverse_transform(preds).tolist()

    return {"prediction": preds[0]}
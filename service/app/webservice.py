import json
import logging
import os
from typing import Optional
import uuid

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from app.utils import load_model
from app.utils import CustomerFeature
import pandas as pd

# Define global variables
SERVICE_NAME = "TelcoChurnService" #os.environ["SERVICE_NAME"]
MODEL_ARTIFACT_PATH = "models/model.pkl" #os.environ["MODEL_ARTIFACT_PATH"]

# Initialize the FastAPI app
app = FastAPI(title=SERVICE_NAME, docs_url="/")

# Configure logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


@app.on_event("startup")
async def startup_load_model():
    global MODEL
    MODEL = load_model(MODEL_ARTIFACT_PATH)


@app.post("/predict")
async def predict(cust_attr: CustomerFeature):
    """Prediction endpoint.
    1. This should be a post request!
    2. Make sure to post the right data.
    """

    response_payload = None

    try:
        # Parse data
        logger.info(f"Input: {str(cust_attr)}")
        input_df = pd.DataFrame([cust_attr.dict()])

        # Define UUID for the request
        request_id = uuid.uuid4().hex

        # Log input data
        logger.info(json.dumps({
            "service_name": SERVICE_NAME,
            "type": "InputData",
            "request_id": request_id,
            "data": input_df.to_json(orient='records')
        }))

        # Make predictions and log
        input_df = input_df.drop('customerId', axis=1)
        model_output = MODEL.predict(input_df).tolist()

        # Log output data
        logger.info(json.dumps({
            "service_name": SERVICE_NAME,
            "type": "OutputData",
            "request_id": request_id,
            "data": model_output
        }))

        # Make response payload
        response_payload = jsonable_encoder(model_output)
    except Exception as e:
        response_payload = {
            "error": str(e)
        }

    return response_payload 
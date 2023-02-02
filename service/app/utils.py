from pydantic import BaseModel
from os import path
import pickle

class CustomerFeature(BaseModel):
    customerId: str
    contract: str
    dependents: str
    deviceProtection: str
    gender: str
    internetService: str
    monthlyCharges: float
    multipleLines: str
    onlineBackup: str
    onlineSecurity: str
    paperlessBilling: str
    partner: str
    paymentMethod: str
    phoneService: str
    seniorCitizen: float
    streamingMovies: str
    streamingTV: str
    techSupport: str
    tenure: float
    totalCharges: float


def load_model(model_artifact_path: str):
    """Loads model artifact from the specified path."""

    if (path.exists(model_artifact_path)):
        with open(model_artifact_path, 'rb') as file:
            model_artifact = pickle.load(file)
        return model_artifact
    else:
        raise FileNotFoundError("The specified path ({model_artifact_path})\
            does not exist.")
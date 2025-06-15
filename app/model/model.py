import os

import joblib
import pandas as pd
from fastapi import Request
from sklearn.ensemble import RandomForestRegressor

MODEL_NAME = "model.joblib"


def load_model() -> RandomForestRegressor:
    """Loads the model from the file system."""
    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, MODEL_NAME)
    return joblib.load(model_path)


def get_model(request: Request) -> RandomForestRegressor:
    """Get the model from the request dependency"""
    return request.state.model


def predict(data: pd.DataFrame, model: RandomForestRegressor) -> pd.DataFrame:
    """Make predictions using the loaded model."""
    return model.predict(data)

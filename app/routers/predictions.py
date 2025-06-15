from enum import Enum

import pandas as pd
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel, FiniteFloat
from sklearn.ensemble import RandomForestRegressor

from app.model.model import get_model, predict
from app.security.authentication import verify_token

PREDICTION_DECIMAL_PRECISION = 8

router = APIRouter()


class OceanProximity(str, Enum):
    """Enumeration of ocean proximity categories."""

    LESS_THAN_1H_OCEAN = "<1H OCEAN"
    INLAND = "INLAND"
    ISLAND = "ISLAND"
    NEAR_BAY = "NEAR BAY"
    NEAR_OCEAN = "NEAR OCEAN"


class HousingPricesParams(BaseModel):
    """Parameters for predict_housing_price."""

    longitude: FiniteFloat
    latitude: FiniteFloat
    housing_median_age: FiniteFloat
    total_rooms: FiniteFloat
    total_bedrooms: FiniteFloat
    population: FiniteFloat
    households: FiniteFloat
    median_income: FiniteFloat
    ocean_proximity: OceanProximity

    def dump_for_prediction(self) -> pd.DataFrame:
        """Dumps the parameters into a DataFrame for prediction."""
        dumped_params = self.model_dump()
        dumped_params.pop("ocean_proximity")

        for proximity in OceanProximity:
            dumped_params[f"ocean_proximity_{proximity.value}"] = int(proximity == self.ocean_proximity)

        return pd.DataFrame([dumped_params])


@router.get("/predict", dependencies=[Depends(RateLimiter(times=5, seconds=5)), Depends(verify_token)])
def predict_housing_price(
    model: RandomForestRegressor = Depends(get_model), params: HousingPricesParams = Depends()
) -> dict:
    """Predict housing price based on the provided params."""
    df = params.dump_for_prediction()
    prediction = predict(df, model)
    return {"prediction": round(prediction[0], PREDICTION_DECIMAL_PRECISION)}

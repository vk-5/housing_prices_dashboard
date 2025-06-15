import copy

import pytest

from tests.conftest import client

VALID_PARAMS = {
    "longitude": -122.64,
    "latitude": 38.01,
    "housing_median_age": 36.0,
    "total_rooms": 1336.0,
    "total_bedrooms": 258.0,
    "population": 678.0,
    "households": 249.0,
    "median_income": 5.5789,
    "ocean_proximity": "NEAR OCEAN",
}

VALID_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQ5MDM1MTYxMzJ9.mtXcwy9PLq9A6ezptz5i52CwM98_FzVH2WxHIcHbrV4"
)
EXPIRED_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDk5MTYyNDh9.Ypjblkjbe1BidHSliAjtnqyJQuqFB5sJWWRIFJONk6g"
)
INVALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOm51bGx9.FFMJXjLYj8Hqusx4ioXGLTN9oFFF7Em6fgKK2hXzmks"


@pytest.mark.asyncio
async def test_predict_not_authenticated(client):
    """
    Test /predictions/predict endpoint without authentication.
    """

    response = client.get("/predictions/predict", params=VALID_PARAMS)

    assert response.status_code == 403

    headers = {"Authorization": f"Bearer {EXPIRED_TOKEN}"}

    response = client.get("/predictions/predict", params=VALID_PARAMS, headers=headers)

    assert response.status_code == 401

    headers = {"Authorization": f"Bearer {INVALID_TOKEN}"}

    response = client.get("/predictions/predict", params=VALID_PARAMS, headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_predict_invalid_params(client):
    """
    Test /predictions/predict endpoint with invalid input params
    """

    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    params = copy.deepcopy(VALID_PARAMS)
    params["longitude"] = "invalidLongitude"

    response = client.get("/predictions/predict", params=params, headers=headers)

    assert response.status_code == 422

    params = copy.deepcopy(VALID_PARAMS)
    params["longitude"] = float("inf")

    response = client.get("/predictions/predict", params=params, headers=headers)

    assert response.status_code == 422

    params = copy.deepcopy(VALID_PARAMS)
    params["ocean_proximity"] = "invalidOceanProximity"

    response = client.get("/predictions/predict", params=params, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_predict_rate_limit(client):
    """
    Test /predictions/predict rate limit
    """

    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}

    for _ in range(5):
        response = client.get("/predictions/predict", params=VALID_PARAMS, headers=headers)

        assert response.status_code == 200

    response = client.get("/predictions/predict", params=VALID_PARAMS, headers=headers)

    assert response.status_code == 429


@pytest.mark.asyncio
async def test_predict(client):
    """
    Test /predictions/predict endpoint
    """

    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}

    response = client.get("/predictions/predict", params=VALID_PARAMS, headers=headers)

    assert response.status_code == 200

    result = response.json()

    assert result["prediction"] == 320201.58554044

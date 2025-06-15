# Housing prices dashboard


## Features
- REST API for housing prices predictions
- Token-based authentication
- Rate limiting based on IP, stored in redis


## Setup
### Local development
- build and run dockerized app with redis, from project root `docker compose --env-file ./conf/local.env up --build`
- for predictions you can use existing token or generate new one (function `create_token` can help)
- valid token for ~36500 days `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODE0NDg4MjB9.rumPDp6leTHsIrVU1gs3PK5VwUlRkfFiuRGnF7xyEd8`
- example
```python
import requests

response = requests.get("http://localhost:8000/monitoring/readiness")
response.raise_for_status()

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODE0NDg4MjB9.rumPDp6leTHsIrVU1gs3PK5VwUlRkfFiuRGnF7xyEd8"
headers = {"Authorization": f"Bearer {token}"}
params = {
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

response = requests.get("http://localhost:8000/predictions/predict", params=params, headers=headers)
response.raise_for_status()
print("✅ Data:", response.json()) 
```

### Other environments
- edit or create `.env` file in the `<project root>/conf` directory, run `docker compose --env-file ./conf/<env>.env up --build`
- prod.env token `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODE0NDg5NTJ9.XvDsjotbvmMhoPlh5kfwUgcVRWB_ey1qUg99UM0d3kA`

### Tests
- run tests from project root `docker compose -f docker-compose.test.yml up --build`
- artifacts are stored in `<project root>/coverage_artifacts` directory

## CI
- first time working with GitHub CI/CD tbh, I have used only GitLab CI/CD before tbh
- runs tests on every push to `main` branch and branch with `Pull request`
- if tests are successful than stores artifacts
- ideally linting and type checking should be added
- next steps would be deploying to dev, test, prod environments (docker registry, k8s or somewhere else)


## Possible improvements and consideration
- I tried to increase python version as high as possible but failed to find compatible version for `scikit-learn` with python version higher than `3.10`
- run uvicorn behind proxy with `--host=127.0.0.1`, for security reasons
- extend JWT tokens with consumer ID, then make rate limiting based on consumer
- use refresh tokens or different algorithm
- I rounded result to 8 decimal digits, to match the given example, internally it has more but but since the results are in tens of thousands, I consider it negligible
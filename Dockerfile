ARG PYTHON=python:3.10-slim

FROM ${PYTHON} AS builder

WORKDIR /housing_prices

COPY conf/logger.yml .

COPY conf/requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000", "--log-config=logger.yml"]

FROM builder AS test

COPY conf/test_requirements.txt .
RUN pip3 install -r test_requirements.txt

COPY tests /housing_prices/tests

WORKDIR /housing_prices

CMD ["python3", "-m", "pytest", "-v"]

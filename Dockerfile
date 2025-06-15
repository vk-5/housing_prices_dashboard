ARG PYTHON=python:3.10-slim

FROM ${PYTHON} AS builder

WORKDIR /housing_prices

COPY conf/logger.yml .

COPY conf/requirements.txt .
RUN pip install --user -r requirements.txt

COPY . .

FROM ${PYTHON} AS release

RUN useradd -m appuser

WORKDIR /housing_prices

COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /housing_prices /housing_prices

ENV PATH="/home/appuser/.local/bin:$PATH" \
    PYTHONPATH="/home/appuser/.local/lib/python3.10/site-packages"

RUN chown -R appuser:appuser /housing_prices
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000", "--log-config=logger.yml"]

FROM builder AS test

RUN useradd -m appuser

WORKDIR /housing_prices

COPY conf/test_requirements.txt .
RUN pip3 install -r test_requirements.txt

COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /housing_prices /housing_prices

COPY tests /housing_prices/tests

ENV PATH="/home/appuser/.local/bin:$PATH" \
    PYTHONPATH="/home/appuser/.local/lib/python3.10/site-packages"

RUN chown -R appuser:appuser /housing_prices
USER appuser

CMD ["/bin/sh", "-c", "coverage run -m pytest -v && coverage xml -o /housing_prices/artifacts/coverage.xml && coverage html -d /housing_prices/artifacts/htmlcov"]

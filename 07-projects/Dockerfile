FROM python:slim-buster

LABEL Description="This image can be used to setup a production-ready FastAPI service."
LABEL maintainer="Hamid Jahani"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade fastapi uvicorn[standard]
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
RUN mlflow server --backend-store-uri postgresql:$DB_POSTGRES --default-artifact-root s3:$S3_Bucket --host $MLFLOW_HOST --no-serve-artifacts
RUN prefect config set PREFECT_API_URL=$PREFECT_API
WORKDIR /app
COPY ./app /app
COPY ./app/data /app/data
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]

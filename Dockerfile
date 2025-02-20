
FROM python:3.9-slim-buster


WORKDIR /app


COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir


COPY . .


EXPOSE 5000




CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "main:app"]

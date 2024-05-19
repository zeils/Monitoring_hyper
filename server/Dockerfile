FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip flask flask-cors requests bs4 schedule

CMD ["python", "main.py"]
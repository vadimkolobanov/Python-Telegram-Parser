FROM python:3.9-alpine

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

WORKDIR /app
CMD ["python", "start.py"]
LABEL authors="Marlen"


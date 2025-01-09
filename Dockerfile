FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk add libpq-dev build-base
RUN pip install --upgrade setuptools wheel

ENV TZ="Europe/Minsk"

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt
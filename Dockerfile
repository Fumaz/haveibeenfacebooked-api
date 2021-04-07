FROM python:3.9-buster

COPY requirements.txt .
RUN pip install -U -r requirements.txt
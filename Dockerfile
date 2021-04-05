FROM python:3.9-buster

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y postgresql
RUN pip install -U flask psycopg2-binary pony
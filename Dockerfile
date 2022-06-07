# syntax=docker/dockerfile:1

FROM python:3.10.4-slim-bullseye

WORKDIR /flask-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "server.py", "--host=0.0.0.0"]
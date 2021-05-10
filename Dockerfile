FROM python:latest

ADD . /python-flask

WORKDIR /python-flask

RUN pip3 install -r requirements.txt



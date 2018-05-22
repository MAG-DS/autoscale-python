FROM python:2.7

RUN apt-get update && apt-get -y install vim

ADD . /autoscale-python

WORKDIR /autoscale-python

RUN pip install -r requirements.txt
FROM python:3.7-alpine
LABEL maintainer="m.mojek@gmail.com"

ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /requirements.txt 
RUN pip install -r /requirements.txt


RUN mkdir /flask_code
WORKDIR /flask_code

COPY . /flask_code/

ENV FLASK_APP /flask_code/app.py
ENV FLASK_ENV=development
ENV CELERY_BROKER_URL='redis://localhost:6379',
ENV CELERY_RESULT_BACKEND='redis://localhost:6379'
RUN adduser -D user
USER user

#EXPOSE 8000
#STOPSIGNAL SIGINT
FROM python:3.7-alpine
LABEL maintainer="m.mojek@gmail.com"

ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /requirements.txt 
RUN pip install -r /requirements.txt


RUN mkdir /flask_code
WORKDIR /flask_code

COPY . /flask_code/

ENV FLASK_APP /flask_code/app/app.py
ENV FLASK_ENV=development

RUN adduser -D user
USER user

#EXPOSE 8000
#STOPSIGNAL SIGINT
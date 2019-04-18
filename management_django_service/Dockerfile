FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /django_code
WORKDIR /django_code
COPY requirements.txt /django_code/
RUN pip install -r requirements.txt
COPY . /django_code/
EXPOSE 8000
STOPSIGNAL SIGINT

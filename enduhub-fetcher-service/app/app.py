from flask import Flask, request
from flask_restful import Api, Resource
from .flask_celery import make_celery

flask_app = Flask(__name__)
api = Api(flask_app)
flask_app.config.update(
    CELERY_BROKER_URL="redis://itra_redis_cache:6379",
    CELERY_RESULT_BACKEND="redis://itra_redis_cache:6379",
)

celery = make_celery(flask_app)

from flask import Flask, request
from flask_restful import Api, Resource
from .flask_celery import make_celery
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration


sentry_sdk.init(
    dsn="https://7afe71258cb849db9589b3079ac9f497@sentry.io/1475386",
    integrations=[FlaskIntegration(), CeleryIntegration()],
)

flask_app = Flask(__name__)
api = Api(flask_app)
flask_app.config.update(
    CELERY_BROKER_URL="redis://datapreparation_redis:6379",
    CELERY_RESULT_BACKEND="redis://datapreparation_redis:6379",
)

celery = make_celery(flask_app)


@flask_app.route("/")
def hello():
    return "Hello data preparation service"


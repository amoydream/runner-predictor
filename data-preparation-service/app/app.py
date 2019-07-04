from flask import Flask, request
from flask_restful import Api, Resource
from .flask_celery import make_celery
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

from .presist_data import PresistData
from .race_event_orientation_preparator import RaceEventOrientationPreparator


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


class DataPreparatorApi(Resource):
    def get(self, race_group_id, redownload):
        race_event_preparator = RaceEventOrientationPreparator(race_group_id)
        prep = PresistData(race_event_preparator)
        if redownload:
            prep = PresistData(race_event_preparator, True)
        data = []
        for row in prep.get_from_redis():
            data.append(row)
        return data


api.add_resource(
    DataPreparatorApi,
    "/race_group/<int:race_group_id>/redownload/<int:redownload>",
)

# @flask_app.route("/")
# def hello():
#     race_group_id = 1
#     race_event_preparator = RaceEventOrientationPreparator(race_group_id)
#     prep = PresistData(race_event_preparator)

#     return "Hello data preparation service"


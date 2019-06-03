from flask import Flask, request
from flask_restful import Api, Resource
from .flask_celery import make_celery
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

from .enduhub_fetcher import EnduhubFetcher
from .enduhub_result_sender import EnduhubResultSender

sentry_sdk.init(
    dsn="https://aedea52e2e4e4f4ca48e57ecad6a019b@sentry.io/1472203",
    integrations=[FlaskIntegration(), CeleryIntegration()],
)

flask_app = Flask(__name__)
api = Api(flask_app)
flask_app.config.update(
    CELERY_BROKER_URL="redis://endu_redis_cache:6379",
    CELERY_RESULT_BACKEND="redis://endu_redis_cache:6379",
)

celery = make_celery(flask_app)


class EnduFetcher(Resource):
    def post(self):
        req_json = request.get_json()
        name = req_json["name"]
        birth = req_json["birth"]

        fetch_data_from_endu.delay(name, birth)

        return "Add to que"


api.add_resource(EnduFetcher, "/")

# celery -A your_application.celery worker
# celery -A app.app.celery worker
@celery.task(name="app.app.fetch_data_from_endu")
def fetch_data_from_endu(name, birth):
    endu = EnduhubFetcher(name, birth)
    endu.prepare_web_links()
    results = endu.fetch_results()
    print("celery")
    for result in results:
        print(result)
        enduhub = EnduhubResultSender(result)
        enduhub.send_data()

    return "done"

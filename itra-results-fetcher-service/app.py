from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class ItraResultFetcher(Resource):
    def post(self):
        req_json = request.get_json()
        return {"hello": req_json["itra_race_id"]}, 201


api.add_resource(ItraResultFetcher, "/")

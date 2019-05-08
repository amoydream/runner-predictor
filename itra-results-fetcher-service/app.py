from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class ItraResultFetcher(Resource):
    def get(self, race_id):
        return {"hello": race_id}


api.add_resource(ItraResultFetcher, "/<string:race_id>")

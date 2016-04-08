from app import api_root
from flask.ext.restful import Resource


@api_root.resource('/v1/')
class HelloAPIV1(Resource):
    def get(self):
        return 'hello, world!'

from flask import Flask, request
from flask_restplus import Resource

from api.restplus import api

ns = api.namespace('first', description='boh')


@ns.route('/')
class ciaoo(Resource):

    def get(self):
        return 'ciaoo', 200

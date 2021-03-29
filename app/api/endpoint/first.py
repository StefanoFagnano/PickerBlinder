from flask import Flask, request
from flask_restplus import Resource

from api.restplus import api

ns = api.namespace('first', description='boh')


@ns.route('/')
class ciaoo(Resource):

    def get(self):
        return 'ciaoo', 200

@ns.route('/upload')
class uploadAPK(Resource):

    def post(self):
        file = request.files['apk']
        injection_type = request.form.get("injecotions")
        return 'ok', 200

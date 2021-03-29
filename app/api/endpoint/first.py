from flask import Flask, request
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage
from api.restplus import api

ns = api.namespace('first', description='boh')


@ns.route('/')
class ciaoo(Resource):

    def get(self):
        return 'ciaoo', 200


from werkzeug.datastructures import FileStorage

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@ns.route('/upload/')
@ns.expect(upload_parser)
class Upload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        return 'ok'+uploaded_file.filename, 200

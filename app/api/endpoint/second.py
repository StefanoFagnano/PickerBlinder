import hashlib
import sys, os, shutil
from flask import Flask, request, send_from_directory, session
from flask_restplus import Resource

from werkzeug.contrib.sessions import Session
from werkzeug.datastructures import FileStorage, CallbackDict
from api.restplus import api

from utils.utils_func import is_apk, save_apk, generate_name, do_json
from utils.disas import disassemble, reassemble, sign
from utils.modify import mainActivity_socket_client
from utils.query import get_last_injection, query

ns = api.namespace('second', description='boh')

upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser.add_argument('injection', type=int, location='form', required=True)


@ns.route('/upload/')
@ns.expect(upload_parser)
class Upload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        if is_apk(uploaded_file.filename):

            injection = args['injection']
            save_apk(uploaded_file)

            uploaded_file.filename = generate_name(uploaded_file)
            print('The name is:' + uploaded_file.filename)

            disassemble(uploaded_file)
            mainActivity_socket_client(uploaded_file, injection)
            reassemble(uploaded_file)
            sign(uploaded_file)
            return do_json('ok', uploaded_file, injection), 200
        else:
            return 415


@ns.param('filename', 'The APK file.')
class download_apk(Resource):

    def get(self, filename):
        return send_from_directory('compile_apk', filename)


ns.add_resource(download_apk, '/download/<path:filename>')

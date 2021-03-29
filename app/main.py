import sys
from flask import Flask, Blueprint
from api.restplus import api
from flask_cors import CORS
from api.restplus import api
from api.endpoint.first import ns as first_namespace

from utils import settings

app = Flask(__name__)
CORS(app)


def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def get_api_blueprint():
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(first_namespace)
    return blueprint


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = get_api_blueprint()
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    try:
        app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.FLASK_DEBUG)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()

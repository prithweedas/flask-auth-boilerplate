from flask import Blueprint, jsonify

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

from flaskrest.api import routes

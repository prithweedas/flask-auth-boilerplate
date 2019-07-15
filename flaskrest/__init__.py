from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, '..', 'app.db')
app.config['SECRET_KEY'] = os.environ['FLASK_REST_SECRET']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

from flaskrest.api import api_blueprint

app.register_blueprint(api_blueprint)


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


import flaskrest.api.auth.models

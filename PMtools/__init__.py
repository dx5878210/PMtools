from flask import Flask
import os

import logging
from config.default import basedir
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')
app.config.from_pyfile('config.py')
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
app.secret_key = os.urandom(32)

handler = logging.FileHandler('log/flask.log', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(handler)


app, logging.info('debug.log',)

db = SQLAlchemy(app)
from PMtools import models


from .api import api
from .mz import mz
from .ddt import ddt
from .hxbns import hxbns
from .index import index
# blueprint
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(mz, url_prefix='/mz')
app.register_blueprint(index, url_prefix='/index')
app.register_blueprint(ddt, url_prefix='/ddt')
app.register_blueprint(hxbns, url_prefix='/hxbns')

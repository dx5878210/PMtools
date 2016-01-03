from flask import Flask


from config.default import basedir
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config.default')
app.config.from_object('instance.config')

db = SQLAlchemy(app)
from PMtools import models


from .api import api
from .mz import mz
from .ddt import ddt
from .index import index
#blueprint
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(mz, url_prefix='/mz')
app.register_blueprint(index, url_prefix='/index')
app.register_blueprint(ddt, url_prefix='/ddt')


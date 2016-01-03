from flask import Blueprint
ddt = Blueprint('ddt', __name__, template_folder='templates')
from . import views

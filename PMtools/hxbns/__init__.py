from flask import Blueprint
hxbns = Blueprint('hxbns', __name__, template_folder='templates')
from . import views
from flask import Blueprint
mz = Blueprint('mz', __name__, template_folder='templates')
from . import views

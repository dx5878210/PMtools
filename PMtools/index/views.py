from . import index
from flask import render_template, redirect


@index.route('/')
def index():
    return render_template('index.html')



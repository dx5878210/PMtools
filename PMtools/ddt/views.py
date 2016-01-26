from . import ddt
from flask import render_template, request, jsonify, flash, redirect, url_for
from PMtools.models import ddtitemscode
from . import text_search, process_file
from werkzeug.utils import secure_filename
import os
from threading import Thread


@ddt.route('/singlesearch/')
def singlesearch():
    return render_template('ddt/singlesearch.html')


@ddt.route('/multiplesearch/')
def multiplesearch():
    return render_template('ddt/multiplesearch.html')


@ddt.route('/multipletextsearch/')
def multipletextsearch():
    return render_template('ddt/multipletextsearch.html')


@ddt.route('/ddtupload/')
def ddtupload():
    return render_template('ddt/fileupload.html')


@ddt.route('/single_search_ajax/', methods=['GET', 'POST'])
def single_search_ajax():
    temp = request.args.get('str')
    # print(temp.isdigit())
    items = ddtitemscode.query.filter(
        ddtitemscode.name.ilike(
            '%' + temp + '%')).all()
    if len(items) == 0:
        print('1')
        items = ddtitemscode.query.filter(
            ddtitemscode.name_id.ilike(
                '%' + temp + '%')).all()
    items_str = ''
    for i in items:
        items_str += (str(i.name) + '\t' + i.name_id + '\n')

    return jsonify(result=items_str)


@ddt.route('/prizetext_search_ajax', methods=['GET', 'POST'])
def prizetext_search_ajax():
    temp = request.args.get('str')
    response_str = text_search.codetable(temp)
    return jsonify(result=response_str)


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@ddt.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    response_str = ''
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(
                os.path.dirname(__file__), 'upload', filename)
            file.save(file_path)
            #response_str='1'
            response_str = process_file.read_send(file_path)
        print (response_str)
    return response_str

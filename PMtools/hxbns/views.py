from . import hxbns
from flask import render_template, request, jsonify, make_response, redirect, url_for, g
from PMtools.models import hxbnsitemscode
from . import text_search, process_file
from werkzeug.utils import secure_filename
import os
from threading import Thread
from functools import wraps


# def allow_cross_domain(func):
#     @wraps(func)
#     def wrapper_func(*args, **kwargs):
#         rst = make_response(func(*args, **kwargs))
#         rst.headers['Access-Control-Allow-Origin'] = '*'
#         rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
#         allow_headers = "Referer,Accept,Origin,User-Agent"
#         rst.headers['Access-Control-Allow-Headers'] = allow_headers
#         return rst
#     return wrapper_func


@hxbns.route('/singlesearch/')
def singlesearch():
    return render_template('hxbns/singlesearch.html')


@hxbns.route('/multipletextsearch/')
def multipletextsearch():
    return render_template('hxbns/multipletextsearch.html')


@hxbns.route('/getvalidateCode/')
def getvalidateCode():
    rm = process_file.RequestsMethods()
    rm.get_cookie()
    #rm.get_validateCode()
    return render_template('hxbns/submitvalidate.html')


@hxbns.route('/hxbnsupload/')
def ddtupload():
    return render_template('hxbns/fileupload.html')


@hxbns.route('/single_search_ajax/', methods=['GET', 'POST'])
def single_search_ajax():
    temp = request.args.get('str')
    # print(temp.isdigit())
    items_name = hxbnsitemscode.query.filter(
        hxbnsitemscode.name.ilike(
            '%' + temp + '%')).all()

    items_names = hxbnsitemscode.query.filter(
        hxbnsitemscode.names.ilike(
            '%' + temp + '%')).all()

    items_id = hxbnsitemscode.query.filter(
        hxbnsitemscode.item_id.ilike(
            '%' + temp + '%')).all()
    # print(type(items_id[0]))
    items = sorted(list(set(items_name + items_names + items_id)),
                   key=lambda item: item.name)

    items_str = ''
    for i in items:
        items_str += (str(i.name) + '\t' + str(i.names) +
                      '\t' + str(i.item_id) + '\n')

    return jsonify(result=items_str)


@hxbns.route('/prizetext_search_ajax', methods=['GET', 'POST'])
def prizetext_search_ajax():
    temp = request.args.get('str')
    response_str = text_search.codetable(temp)
    return jsonify(result=response_str)


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@async
@hxbns.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    response_str = ''
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(
                os.path.dirname(__file__), 'upload', filename)
            file.save(file_path)
            response_str = process_file.read_send(file_path)
    return jsonify(result=response_str)

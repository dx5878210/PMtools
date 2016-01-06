from . import ddt
from flask import render_template, request, jsonify
from PMtools.models import ddtitemscode
from . import text_search


@ddt.route('/singlesearch/')
def singlesearch():
    return render_template('ddt/singlesearch.html')


@ddt.route('/multiplesearch/')
def multiplesearch():
    return render_template('ddt/multiplesearch.html')


@ddt.route('/multipletextsearch/')
def multipletextsearch():
    return render_template('ddt/multipletextsearch.html')


@ddt.route('/single_search_ajax/', methods=['GET', 'POST'])
def single_search_ajax():
    temp = request.args.get('str')
    #print(temp.isdigit())
    items = ddtitemscode.query.filter(
            ddtitemscode.name.ilike(
                '%' + temp + '%')).all()
    items_str = ''
    for i in items:
        items_str += (str(i.name) + '\t' + i.name_id + '\n')

    return jsonify(result=items_str)


@ddt.route('/prizetext_search_ajax', methods=['GET', 'POST'])
def prizetext_search_ajax():
    temp = request.args.get('str')
    response_str=text_search.codetable(temp)
    return jsonify(result=response_str)
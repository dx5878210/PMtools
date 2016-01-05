from . import mz
from flask import render_template, request, jsonify
from PMtools.models import mzitemscode
from . import text_search


@mz.route('/singlesearch/')
def singlesearch():
    return render_template('mz/singlesearch.html')


@mz.route('/multiplesearch/')
def multiplesearch():
    return render_template('mz/multiplesearch.html')


@mz.route('/multipletextsearch/')
def multipletextsearch():
    return render_template('mz/multipletextsearch.html')


@mz.route('/single_search_ajax/', methods=['GET', 'POST'])
def single_search_ajax():
    temp = request.args.get('str')
    #print(temp.isdigit())
    if temp.isdigit() == True:
        items = mzitemscode.query.filter(
            mzitemscode.uid.ilike(
                '%' + temp + '%')).all()
    else:
        items = mzitemscode.query.filter(
            mzitemscode.name.ilike(
                '%' + temp + '%')).all()
    items_str = ''
    for i in items:
        items_str += (str(i.uid) + '\t' + i.name + '\n')

    return jsonify(result=items_str)


@mz.route('/prizetext_search_ajax', methods=['GET', 'POST'])
def prizetext_search_ajax():
    temp = request.args.get('str')
    response_str = text_search.codetable(temp)
    return jsonify(result=response_str)

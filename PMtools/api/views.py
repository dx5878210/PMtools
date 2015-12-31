from . import api


@api.route('/se')
def search():
    return 'Hello api!'


@api.route('/')
def api1():
    return 'Hello a'

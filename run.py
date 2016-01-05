from PMtools import app
from flask.ext.script import Manager,Server
#hooks test1
manager = Manager(app)
manager.add_command(
    "runserver",
    Server(
        host="127.0.0.1",
        port=8181,
        use_debugger=True))
if __name__ == '__main__':
    manager.run()
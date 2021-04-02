import json

from flask import Flask
from flask import request
from service import ToDoService


app = Flask(__name__)
service = ToDoService()


@app.route('/todo/', methods=['POST'])
def create_todo():
    return service.create(params=json.loads(request.get_data()))


@app.route('/todo/')
@app.route('/todo/<int:pk>/', methods=['GET'])
def retrieve_item(pk=None):
    if pk:
        return service.retrieve(pk)
    else:
        return service.list()


@app.route('/todo/<string:method>/<int:pk>/', methods=['POST'])
def modify_item(method, pk):
    if method == "delete":
        return service.delete_todo(pk)
    elif method == "done":
        return service.done_todo(pk)
    else:
        return "404"


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

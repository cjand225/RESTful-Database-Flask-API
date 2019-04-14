from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

# export FLASK_APP=CS405GFinalPython:app
# flask run
app = Flask(__name__)

db_host = 'cjan225.netlab.uky.edu'
db_user = 'projectuser'
db_pass = 'cs405'
db_name = 'classproject'

db_connect = engine = create_engine('mysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/status')
def getStatus():
    conn = db_connect.connect()
    status = {"status_code": -1}
    if conn.connection:
        status = {"status_code": 1}
    elif conn.closed:
        status = {"status_code": 0}

    return jsonify(status)


if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

app = Flask(__name__)

db_host = 'cjan225.netlab.uky.edu'
db_user = 'projectuser'
db_pass = 'cs405'
db_name = 'classproject'

db_connect = engine = create_engine('mysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name)
app = Flask(__name__)
api = Api(app)


class getStatus(Resource):
    def get(self):
        result = {'status': 1}
        return jsonify(result)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/status')
def getStatus():
    return


if __name__ == '__main__':
    app.run()

#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_host = 'cjan225.netlab.uky.edu, port 3306'
db_user = 'projectuser'
db_pass = 'cs405'
db_name = 'classproject'

db_connect = engine = create_engine('mysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name)
app = Flask(__name__)
api = Api(app)

from flask_restful import Resource, Api

class getPatient(Resource):
    def get(self, pid):
        conn = db_connect.connect()



#api.add_resource(Service, )


if __name__ == '__main__':
    app.run()

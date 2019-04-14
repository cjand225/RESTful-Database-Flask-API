#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_host = ''
db_user = ''
db_pass = ''
db_name = ''

db_connect = engine = create_engine('mysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name)
app = Flask(__name__)
api = Api(app)


class Service(Resource):
    def get(self, service_id):
        pass

    def remove(self, service_id):
        pass

    def add(self, ):
        pass


class Provider(Resource):
    def get(self, npi):
        pass

    def remove(self, npi):
        pass

    def add(self, ):
        pass


class Patient(Resource):
    def get(self, npi):
        pass

    def remove(self, npi):
        pass

    def add(self, ):
        pass


class PatientData(Resource):
    def get(self, npi):
        pass

    def add(self, ):
        pass


api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Tracks, '/tracks')  # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3

if __name__ == '__main__':
    app.run()

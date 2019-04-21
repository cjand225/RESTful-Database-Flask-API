from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from json import dumps

from db import Base, Location, Department, Provider, Patient, Data, Service, Institution
# from newdb import metadata, location, department, provider, patient, data, service, institution

from sqlalchemy import create_engine, ForeignKey, Table, MetaData, Column, Integer, String, DateTime, inspect, delete, \
    select, insert, schema, types
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import IntegrityError
import uuid

# db_user = 'projectuser'
# db_pass = 'cs405'
# db_name = 'classproject'

db_host = 'cjan225.netlab.uky.edu'
db_user = 'testuser'
db_pass = 'test'
db_name = 'testdb'

db = {'drivername': 'mysql',
      'username': 'testuser',
      'password': 'test',
      'host': 'cjan225.netlab.uky.edu',
      'port': 3306,
      'database': 'testdb'}

url = URL(**db)
app = Flask(__name__)
engine = create_engine(url)
api = Api(app)

# -------DB declarations--------


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print('DB Created!')
print(engine.url)


# ---------API-------------------
@app.route('/')
def welcome():
    return "I think you're lost :)"


@app.route('/api')
def apiEndPoint():
    return "Team API"


@app.route('/api/status', methods=['GET'])
def getStatus():
    conn = engine.connect()
    status = {"status_code": -1}
    if not conn.closed:
        status = {"status_code": 1}
    elif conn.closed:
        status = {"status_code": 0}
    return jsonify(status)


# Get--------------------------------------------------------
@app.route('/api/getservice/<service_id>', methods=['GET'])
def getService(service_id):
    if request.method == "GET":
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        query = currSession.query(Service, Service.id).filter(Service.id == service_id)
        query.join(Service.location)
        print(query)
        result = currSession.execute(query)
        response = giveResponse(result)
        currSession.commit()
        currSession.close()
        return jsonify(response)


@app.route('/api/getpatient/<patient_id>', methods=['GET'])
def getPatient(patient_id):
    if request.method == "GET":
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        query = currSession.query(Service, Patient.pid).filter_by(id=patient_id)
        result = currSession.execute(query)
        response = giveResponse(result)
        currSession.commit()
        currSession.close()
        return jsonify(response)


@app.route('/api/getprovider/<provider_id>', methods=['GET'])
def getProvider(provider_id):
    if request.method == "GET":
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        query = currSession.query(Provider, Provider.npi).filter_by(id=provider_id)
        result = currSession.execute(query)
        response = giveResponse(result)
        currSession.commit()
        currSession.close()
        return jsonify(response)


@app.route('/api/getdata/<data_id>', methods=['GET'])
def getData(data_id):
    if request.method == "GET":
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        query = currSession.query(Data, Data.id).filter_by(id=data_id)
        result = currSession.execute(query)
        response = giveResponse(result)
        currSession.commit()
        currSession.close()
        return jsonify(response)


# Add--------------------------------------------
@app.route('/api/addservice', methods=['POST'])
def addService():
    if request.method == "POST":
        data = request.get_json(force=True)
        attempted_address = data['address']
        attempted_dept = data['department_id']
        attempted_service = data['service_id']
        attempted_tax = data['taxid']

        result = ''
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()

        nLocation = Location(address=attempted_address)

        nInstitution = Institution(tid=attempted_tax)
        nDepartment = Department(id=attempted_dept, institution_id=nInstitution.id)

        try:
            result = currSession.add_all([nLocation, nDepartment, nInstitution])
        except IntegrityError:
            pass
        finally:
            currSession.commit()

        nService = Service(id=attempted_service, department_id=nDepartment.id, location_id=nLocation.lid)

        try:
            result = currSession.add_all([nService])
        except IntegrityError:
            pass
        finally:
            currSession.commit()
            currSession.close()

        response = giveResponse(result)
        return jsonify(response)


@app.route('/api/addpatient/', methods=['POST'])
def addPatient():
    if request.method == "POST":
        data = request.get_json(force=True)
        attempted_address = data['address']
        attempted_provider = data['provider_id']
        attempted_pid = data['pid']
        attempted_ssn = data['ssn']
        lid = uuid.uuid4()

        response = dbAdd([])
        return jsonify(response)


@app.route('/api/addprovider/', methods=['POST'])
def addProvider():
    if request.method == "POST":
        data = request.get_json(force=True)
        attempted_dept = data['department_id']
        attempted_npi = data['npi']

        nProvider = Provider()

        response = dbAdd([])
        return jsonify(response)


@app.route('/api/adddata/', methods=['POST'])
def addData():
    if request.method == "POST":
        data = request.get_json(force=True)
        attempted_data = data['data']
        attempted_pid = data['patient_id']
        attempted_sid = data['service_id']
        attempted_provid = data['provider_id']
        attempted_did = data['id']
        response = dbAdd([])
        return jsonify(response)


# Remove-----------------------------------------
@app.route('/api/removeservice/<service_id>', methods=['GET'])
def removeService(service_id):
    if request.method == "GET":
        deleteQuery = delete(Service, Service.id == service_id)
        response = dbDelete(deleteQuery)
        return jsonify(response)


@app.route('/api/removepatient/<pid>', methods=['GET'])
def removePatient(pid):
    if request.method == "GET":
        deleteQuery = delete(Patient, Patient.pid == pid)
        response = dbDelete(deleteQuery)
        return jsonify(response)


@app.route('/api/removeprovider/<npi>', methods=['GET'])
def removeProvider(npi):
    if request.method == "GET":
        deleteQuery = delete(Provider, Provider.npi == npi)
        response = dbDelete(deleteQuery)
        return jsonify(response)


def dbDelete(query):
    result = ''
    sessionMake = sessionmaker(bind=engine)
    currSession = sessionMake()
    try:
        result = currSession.delete(query)
    except IntegrityError:
        pass
    finally:
        currSession.commit()
        currSession.close()
        return giveResponse(result)


def dbAdd(query):
    result = ''
    sessionMake = sessionmaker(bind=engine)
    currSession = sessionMake()
    try:
        result = currSession.add_all(query)
    except IntegrityError:
        pass
    finally:
        currSession.commit()
        return result


def giveResponse(result):
    response = {}

    if result:
        if result.returns_rows and result.rowcount > 0:
            for row in result.fetchall():
                response.update(row)
        elif result.rowcount == 0:
            response.update({'Error': 'Not Found'})
    else:
        response.update({'Status': '1'})

    return response


if __name__ == '__main__':
    app.run()

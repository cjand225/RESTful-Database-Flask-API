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
            result = currSession.add(nService)
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
       
        result = ''
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        nProvider = Provider(npi=attempted_provider)

        try:
            result = currSession.add_all([nProvider])
        except IntegrityError:
            pass
        finally:
            currSession.commit()

        nPatient = Patient(pid=attempted_pid,ssn=attempted_ssn,address=attempted_address,provider_id = nProvider.npi)

        try:
            result = currSession.add_all([nPatient])
        except IntegrityError:
            pass
        finally:
            currSession.commit()
            currSession.close()

        response = giveResponse(result)
        return jsonify(response)


@app.route('/api/addprovider/', methods=['POST'])
def addProvider():
    if request.method == "POST":
        data = request.get_json(force=True)
        attempted_dept = data['department_id']
        attempted_npi = data['npi']
       
        result = ''
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        nDepartment = Department(id=attempted_dept)


        try:
            result = currSession.add_all([nDepartment])
        except IntegrityError:
            pass
        finally:
            currSession.commit()

        nProvider = Provider(npi=attempted_npi,department_id=nDepartment.id)

        try:
            result = currSession.add_all([nProvider])
        except IntegrityError:
            pass
        finally:
            currSession.commit()
            currSession.close()

        response = giveResponse(result)
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
       
        result = ''
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        nPatient = Patient(pid=attempted_pid)
        nService = Service(id=attempted_sid)
        nProvider = Provider(npi=attempted_provid)

        try:
            result = currSession.add_all([nPatient,nService,nProvider])
        except IntegrityError:
            pass
        finally:
            currSession.commit()

        nData = data(id=attempted_did, patient_id=nPatient.pid,service_id=nService.id)

        try:
            result = currSession.add_all([nData])
        except IntegrityError:
            pass
        finally:
            currSession.commit()
            currSession.close()

        response = giveResponse(result)
        return jsonify(response)


# Remove-----------------------------------------
@app.route('/api/removeservice/<service_id>', methods=['GET'])
def removeService(service_id):
    if request.method == "GET":
        return dbDelete(Service, service_id)


@app.route('/api/removepatient/<pid>', methods=['GET'])
def removePatient(pid):
    if request.method == "GET":
        return dbDelete(Patient, pid)


@app.route('/api/removeprovider/<npi>', methods=['GET'])
def removeProvider(npi):
    if request.method == "GET":
        return dbDelete(Provider, npi)


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


def dbDelete(table, id):
    result = ''
    sessionMake = sessionmaker(bind=engine)
    currSession = sessionMake()

    try:
        row = currSession.query(table).get(id)
        print(row)
        result = currSession.delete(row)
    except IntegrityError:
        pass
    finally:
        currSession.commit()
        currSession.close()

    response = giveResponse(result)
    return jsonify(response)


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

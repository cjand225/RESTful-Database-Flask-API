from flask import Flask, request, jsonify
from flask_restful import Api

import datetime
from App.db import Base, Location, Department, Provider, Patient, Data, Service, Institution
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import IntegrityError

# db_user = 'projectuser'
# db_pass = 'cs405'
# db_name = 'classproject'

db_host = 'cjan225.netlab.uky.edu'
db_user = 'testuser'
db_pass = 'test'
db_name = 'testdb'

db = {'drivername': 'mysql',
      'username': 'projectuser',
      'password': 'cs405',
      'host': 'cjan225.netlab.uky.edu',
      'port': 3306,
      'database': 'classproject'}

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
        return dbGet(Service, service_id)


@app.route('/api/getpatient/<patient_id>', methods=['GET'])
def getPatient(patient_id):
    if request.method == "GET":
        return dbGet(Patient, patient_id)


@app.route('/api/getprovider/<provider_id>', methods=['GET'])
def getProvider(provider_id):
    if request.method == "GET":
        return dbGet(Provider, provider_id)


@app.route('/api/getdata/<data_id>', methods=['GET'])
def getData(data_id):
    if request.method == "GET":
        return dbGet(Data, data_id)


# Add--------------------------------------------
@app.route('/api/addservice', methods=['POST'])
def addService():
    if request.method == "POST":
        data = request.get_json(force=True)

        # check if valid amount and correct parameters given
        params = ['address', 'department_id', 'service_id', 'taxid']
        if not all(name in data for name in params):
            return jsonify({'Status': '0', 'Error': 'Invalid Amount of Parameters'})

        attempted_address = data['address']
        attempted_dept = data['department_id']
        attempted_service = data['service_id']
        attempted_tax = data['taxid']

        if dbExists(Service, attempted_service):
            return jsonify({'Status': '0', 'Error': 'Query Exists already in DB'})

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

        # check if valid amount and correct parameters given
        params = ['address', 'provider_id', 'pid', 'ssn']
        if not all(name in data for name in params):
            return jsonify({'Status': '0', 'Error': 'Invalid Amount of Parameters'})

        attempted_address = data['address']
        attempted_provider = data['provider_id']
        attempted_pid = data['pid']
        attempted_ssn = data['ssn']

        if dbExists(Patient, attempted_pid):
            return jsonify({'Status': '0', 'Error': 'Query Exists already in DB'})

        result = ''
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        nProvider = Provider(id=attempted_provider)

        try:
            result = currSession.add_all([nProvider])
        except IntegrityError:
            pass
        finally:
            currSession.commit()

        nPatient = Patient(id=attempted_pid, ssn=attempted_ssn, address=attempted_address, provider_id=nProvider.id)

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

        # check if valid amount and correct parameters given
        params = ['department_id', 'npi']
        if not all(name in data for name in params):
            return jsonify({'Status': '0', 'Error': 'Invalid Amount of Parameters'})

        attempted_dept = data['department_id']
        attempted_npi = data['npi']

        if dbExists(Provider, attempted_npi):
            return jsonify({'Status': '0', 'Error': 'Query Exists already in DB'})

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

        nProvider = Provider(id=attempted_npi, department_id=nDepartment.id)

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

        # check if valid amount and correct parameters given
        params = ['data', 'patient_id', 'service_id', 'provider_id', 'id']
        if not all(name in data for name in params):
            return jsonify({'Status': '0', 'Error': 'Invalid Amount of Parameters'})

        attempted_data = data['data']
        attempted_pid = data['patient_id']
        attempted_sid = data['service_id']
        attempted_provid = data['provider_id']
        attempted_did = data['id']

        if dbExists(Data, attempted_did):
            return jsonify({'Status': '0', 'Error': 'Query Exists already in DB'})

        result = ''
        sessionMake = sessionmaker(bind=engine)
        currSession = sessionMake()
        nPatient = Patient(id=attempted_pid)
        nService = Service(id=attempted_sid)
        nProvider = Provider(id=attempted_provid)

        try:
            result = currSession.add_all([nPatient, nService, nProvider])
        except IntegrityError:
            pass
        finally:
            currSession.commit()

        nData = Data(id=attempted_did, patient_id=nPatient.id, service_id=nService.id, some_data=attempted_data,
                     ts=datetime.datetime.utcnow())

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


def dbGet(table, id):
    sessionMake = sessionmaker(bind=engine)
    currSession = sessionMake()
    query = currSession.query(table, table.id).filter(table.id == id)
    print(query)
    result = currSession.execute(query)
    response = giveResponse(result)
    currSession.commit()
    currSession.close()
    return jsonify(response)


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


def dbExists(table, id):
    response = False
    sessionMake = sessionmaker(bind=engine)
    currSession = sessionMake()
    query = currSession.query(table, table.id).filter(table.id == id)
    result = currSession.execute(query)
    currSession.commit()
    currSession.close()

    if result:
        if result.returns_rows and result.rowcount > 0:
            response = True

    return response


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

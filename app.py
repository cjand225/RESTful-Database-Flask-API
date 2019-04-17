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

db_connect = create_engine('mysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name)
api = Api(app)


@app.route('/')
def welcome():
    return "I think you're lost :)"


@app.route('/api')
def apiEndPoint():
    return "Team API"


@app.route('/api/status', methods=['GET'])
def getStatus():
    conn = db_connect.connect()
    status = {"status_code": -1}
    if not conn.closed:
        status = {"status_code": 1}
    elif conn.closed:
        status = {"status_code": 0}

    return jsonify(status)


# Get--------------------------------------------------------
@app.route('/api/getservice/<int:service_id>', methods=['GET'])
def getService(service_id):
    if request.method == "GET":
        serv_id = service_id
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)


@app.route('/api/getpatient/<int:patient_id>', methods=['GET'])
def getPatient(patient_id):
    if request.method == "GET":
        pid = patient_id
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)


@app.route('/api/getprovider/<int:provider_id>', methods=['GET'])
def getProvider(provider_id):
    if request.method == "GET":
        prov_id = provider_id
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)



@app.route('/api/getdata/<int:data_id>', methods=['GET'])
def getData(data_id):
    if request.method == "GET":
        dat_id = data_id
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)


# Add--------------------------------------------
@app.route('/api/addservice/', methods=['POST'])
def addService():
    if request.method == "POST":
        attempted_address = request.form['address']
        attempted_dept = request.form['department_id']
        attempted_service = request.form['service_id']
        attempted_tax = request.form['taxid']
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)


@app.route('/api/addpatient/', methods=['POST'])
def addPatient():
    if request.method == "POST":
        attempted_address = request.form['address']
        attempted_provider = request.form['provider_id']
        attempted_pid = request.form['pid']
        attempted_ssn = request.form['ssn']
        response = 'NULL'
        return jsonify(response)


@app.route('/api/addprovider/', methods=['POST'])
def addProvider():
    if request.method == "POST":
        attempted_dept = request.form['department_id']
        attempted_npi = request.form['npi']
        response = 'NULL'
        return jsonify(response)


@app.route('/api/adddata/', methods=['POST'])
def addData():
    if request.method == "POST":
        attempted_data = request.form['data']
        attempted_pid = request.form['patient_id']
        attempted_sid = request.form['service_id']
        attempted_provid = request.form['provider_id']
        attempted_did = request.form['id']
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)



# Remove-----------------------------------------
@app.route('/api/removeservice/<int:service_id>', methods=['GET'])
def removeService(service_id):
    if request.method == "GET":
        idRemoved = service_id
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)


@app.route('/api/removepatient/<int:pid>', methods=['GET'])
def removePatient(pid):
    if request.method == "GET":
        pidRemvoed = pid
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)


@app.route('/api/removeprovider/<int:npi>', methods=['GET'])
def removeProvider(npi):
    if request.method == "GET":
        npiRemoved = npi
        # do stuff here with it
        response = 'NULL'
        return jsonify(response)


if __name__ == '__main__':
    app.run()

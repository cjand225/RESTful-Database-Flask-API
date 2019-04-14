@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/status')
def getStatus():
    return
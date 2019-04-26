# Flask Database API  
## DB Table Layout  
    () unique,     <> Primary
    Patient:   (SSN), <(PID)>, address, Current provider
    Provider:  <(NPI)>, 0...N patient, current primary dep
    Departments:   Institution, 1...N provider, 1...N locatin
    Institution:   <(Tax ID)>, 1...N location, 1...N dep
    Service:       location, dep, inst
    Location:      1 address
    Data Source    <(Id)>, timestamp, 1 patient and 1 service

## Requirements to Run
    Python 3.7
    flask
    flask_restful
    SQLAlchemy
    mysqlclient
    

## Linux Commands
    export FLASK_APP=[__main__.py program location]
    flask run

## Tested for:
    Duplicate Entries
    Incorrect Parameters
    Incorrent Amount of Parameters

## Notes

Not a lot of testing was done, but testing scripts and an semi-automated testing can be found in /scripts folder

Make sure to put any scripts you want to test in scripts/tests, then you can just use the following:

    runTests.sh
    
Which will run any script located in that folder and output each one into a separate log inside the scripts/logs folder for convenience.
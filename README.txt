# () unique,     <> Primary
# Patient:   (SSN), <(PID)>, address, Current provider
# Provider:  <(NPI)>, 0...N patient, current primary dep
# Departments:   Institution, 1...N provider, 1...N locatin
# Institution:   <(Tax ID)>, 1...N location, 1...N dep
# Service:       location, dep, inst
# Location:      1 address
# Data Source    <(Id)>, timestamp, 1 patient and 1 service


# export FLASK_APP=CS405GFinalPython:app
# flask run
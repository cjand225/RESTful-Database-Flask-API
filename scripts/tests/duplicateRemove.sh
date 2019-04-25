#!/usr/bin/env bash

curl -d '{"address":"800 Rose Street.","department_id":"d-0","service_id":"s-0","taxid":"8808-080"}'  \
     -H "Content-Type: application/json" \
     -X POST http://localhost:5000/api/addservice
wait
curl http://localhost:5000/api/removeservice/s-0
wait
curl http://localhost:5000/api/removeservice/s-0
wait
curl -d '{"department_id":"d-0","npi":"n-000-000"}' \
     -H "Content-Type: application/json" \
     -X POST http://localhost:5000/api/addprovider
wait
curl http://localhost:5000/api/removeprovider/n-000-000
wait
curl http://localhost:5000/api/removeprovider/n-000-000
#!/usr/bin/env bash

curl http://localhost:9990/api/removeservice/p-0-0-0
wait
curl http://localhost:9990/api/removeservice/b2el1s
wait
curl http://localhost:9990/api/removepatient/n-000-000
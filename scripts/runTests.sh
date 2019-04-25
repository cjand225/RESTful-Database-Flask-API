#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
if [ ! -d $DIR/logs ];then
    sh -c "mkdir $DIR/logs"
fi

for filename in $DIR/tests/*.sh; do
    sh -x $filename >> "logs/$(basename "$filename" .sh).log"
    sleep 5
done
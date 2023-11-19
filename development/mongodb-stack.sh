#!/bin/bash
D=$(dirname "$0")
docker-compose -p smpr-mongo -f "$D/mongodb-stack.yml" "$@"
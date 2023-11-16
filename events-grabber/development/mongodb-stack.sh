#!/bin/bash
D=$(dirname $0)
docker-compose -p dg-external -f "$D/mongodb-stack.yml" "$@"
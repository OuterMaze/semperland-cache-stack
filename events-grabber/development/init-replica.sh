#!/bin/bash
set -e

cp /etc/mongo/keyfile-source /etc/mongo/keyfile
chmod 0400 /etc/mongo/keyfile

if [ "$MONGO_INITDB_ROOT_USERNAME" ] && [ "$MONGO_INITDB_ROOT_PASSWORD" ]; then
    "${mongo[@]}" -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --eval 'rs.initiate()'
fi
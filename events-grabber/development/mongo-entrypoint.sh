cp /etc/mongo/keyfile-source /etc/mongo/keyfile
chmod 0400 /etc/mongo/keyfile
mongod --replSet rs0 --keyFile "/etc/mongo/keyfile"

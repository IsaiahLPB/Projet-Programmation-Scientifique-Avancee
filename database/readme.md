# The database need a "user0" to be called, to do so, you have to

systemctl start mongod.service

mongosh mongodb://127.0.0.1

use results

db.createUser({ user: "user0", pwd: "pwd0", roles: ["dbAdmin"]})

# If you want to see what is in your DB

db.matrix.find()
from pymongo import MongoClient
from collections import OrderedDict
from .constant import DB_URL

conn = MongoClient(DB_URL)
db = conn.techquiz

if len(db.collection_names()) < 1:
    db.create_collection('user')
        
vexpr = {"$jsonSchema":
      {
             "bsonType": "object",
             "required": [ "username", "email", "password" ],
             "properties": {
                "username": {
                   "bsonType": "string",
                   "description": "must be a string and is required"
                },
                "email": {
                   "bsonType": "string",
                   "description": "must be a string and is required"
                },
                "password": {
                   "bsonType": "string",
                   "description": "must be a string and is required",
                   "minLength":7
                },
                "admin":{
                    "bsonType":"bool",
                    "description": "must be a boolean and is not required",
                },
                "score":{
                    "bsonType":"int",
                    "description": "must be a int and is not required",
                },
                "friends":{
                    "bsonType":"array",
                    "description":"must be array and is not required"
                },
                "createdAt":{
                    "bsonType":"date",
                    "description": "must be a date and is not required",
                }
             }
      }
    }

cmd = OrderedDict([('collMod', 'user'),
            ('validator', vexpr),
            ('validationLevel', 'moderate')])
    
db.command(cmd)

db.user.create_index("email", unique=True)

# 4 different collections for question

python = db.python
java = db.java
c = db.c
cpp = db.cpp
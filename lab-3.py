from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from marshmallow import Schema, fields
from bson.json_util import dumps
from json import loads
from keys import keys
import datetime

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://admin:"+keys["pw"]+"@cluster0.41j7h.mongodb.net/"+keys["nm"]+"?retryWrites=true&w=majority"
mongo = PyMongo(app)

db_operations = mongo.db.tanks
dte = datetime.datetime.now()

profileDB = {
    "sucess": True,
    "data": {
        "last_updated": "2/3/2021, 8:48:51 PM",
        "username": "coolname",
        "role": "Engineer",
        "color": "#3478ff"
    }
}

class TankSchema(Schema):
  location = fields.String(required=True)
  lat = fields.Float(required=True)
  long = fields.Float(required=True)
  percentage_full = fields.Integer(required=True)

@app.route("/", methods=["GET"])
def home():
    return "hello lab 3"

# PROFILE Routes:
@app.route("/profile", methods=["GET", "POST", "PATCH"])
def profile():
    if request.method == "POST":
        # /POST
        profileDB["data"]["last_updated"] = (dte.strftime("%c"))
        profileDB["data"]["username"] = (request.json["username"])
        profileDB["data"]["role"] = (request.json["role"])
        profileDB["data"]["color"] = (request.json["color"])
       
        return jsonify(profileDB)
   
    elif request.method == "PATCH":
        # /PATCH
        profileDB["data"]["last_updated"] = (dte.strftime("%c"))
        
        tempDict = request.json
        attributes = tempDict.keys()
        
        for attribute in attributes:
            profileDB["data"][attribute] = tempDict[attribute]
  
        return jsonify(profileDB)

    else:
        # /GET
        return jsonify(profileDB)

# DATA Routes:
@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        # /POST
        newTank = TankSchema().load(request.json)

        db_operations.insert_one(newTank)
        return loads(dumps(newTank))

    else:
        # /GET

        tanks = db_operations.find()
        return  jsonify(loads(dumps(tanks)))


@app.route("/data/<ObjectId:id>", methods=["PATCH", "DELETE"])
def update(id):

    filt = {"_id" : id}

    if request.method == "PATCH":
        # /PATCH
       
        updates = {"$set": request.json}
        db_operations.update_one(filt, updates)      
        
        updatedTank = db_operations.find_one(filt)
        return  jsonify(loads(dumps(updatedTank)))

    elif request.method == "DELETE":
        # /DELETE

        tmp = db_operations.delete_one(filt)
        
        result = {"sucess" : True} if tmp.deleted_count == 1 else {"sucess" : False}
        return result

    else:
        # /GET

        tanks = db_operations.find()
        return  jsonify(loads(dumps(tanks)))

# Main
if __name__ == '__main__':
   app.run(debug = True)

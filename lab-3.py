from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

app.config["MONGO_URI"] = "<YOUR_CONNECTION_STRING>"
mongo = PyMongo(app)

dte = datetime.datetime.now()

db_operations = mongo.db.tanks

profileDB = {
    "sucess": True,
    "data": {
        "last_updated": "2/3/2021, 8:48:51 PM",
        "username": "coolname",
        "role": "Engineer",
        "color": "#3478ff"
    }
}

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
        
        posts = {}
        posts["location"] = (request.json["location"])
        posts["lat"] = (request.json["lat"])
        posts["long"] = (request.json["long"])
        posts["percentage_full"] = (request.json["percentage_full"])

        db_operations.insert_one(jsonify(posts))
        return jsonify(posts)

    else:
        # /GET

        tanks = db_operations.find()
        return jsonify(tanks)

@app.route("/data/<ObjectId:id>", methods=["PATCH", "DELETE"])
def update(id):

    filt = {"_id" : id}

    if request.method == "PATCH":
        # /PATCH
       
        updatedTank = {"$set": request.json}
        
        db_operations.update_one(filt, updatedTank)      
        return jsonify(updatedTank) 

    elif request.method == "DELETE":
        # /DELETE

        tmp = db_operations.delete_one(filt)
        
        result = {"sucess" : True} if tmp.deleted_count == 1 else {"sucess" : False}
        return result

    else:
        # /GET

        tanks = db_operations.find()
        return jsonify(tanks)

# Main
if __name__ == '__main__':
   app.run(debug = True)

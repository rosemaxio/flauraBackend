from dotenv import load_dotenv
import os
from flask import request, Response
from bson.json_util import dumps
import json
import pymongo

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
DATABASE_URL = f'mongodb+srv://{os.environ.get("dbUser")}:{os.environ.get("dbPasswort")}' \
               '@flask-mongodb-atlas.wicsm.mongodb.net/' \
               'flaura?retryWrites=true&w=majority'  # get connection url from environment

client = pymongo.MongoClient(DATABASE_URL)  # establish connection with database

mydb = client.flaura
mycol = mydb.users


def jsonResponse(data):
    return Response(data, mimetype='application/json')


def getUserByPlantToken(token):
    susUser = mycol.find_one({"pots.token": token})
    if susUser == None:
        return "noUser"
    else:
        return susUser

# Updates the field <name> of Pot with Token <token> to <newValue>
# TODO maybe add all changes to a new database, for history (e.g. moisture of pot in the last 14 days)
def updateTestValue(token, name, newValue):
    newData = getUserByPlantToken(token)
    if newData != "noUser":
        for pot in newData["pots"]:
            if pot["token"] == token:
                pot[name] = newValue;
        mycol.save(newData) # could probably also use update
        return 'success'
    return "Something went wrong... Is the Token set correctly?"

def getTestValue(token, name):
    newData = getUserByPlantToken(token)
    if newData != "noUser":
        for pot in newData["pots"]:
            if pot["token"] == token:
                return jsonResponse(dumps(pot[name]))
    return "Something went wrong... Is the Token set correctly?"
# getCorrect Person entry via current Token
# then find the right plant via plant token
# then get the value there
# and change it
'''
pipeline = [
    { $filter: {
               input: "$pots",
               as: "item",
               cond: { $eq: [ "$$item.token", "abc" ] }
            }
         }
} }}]

def getTestValue(token):
    testentry = mycol.aggregate()
    return testentry.

/**
 * specifications: The fields to
 *   include or exclude.
 */
{ $project
     pots: {
            $filter: {
               input: "$pots",
               as: "item",
               cond: { $eq: [ "$$item.token", "abc" ] }
            }
         }
}
'''

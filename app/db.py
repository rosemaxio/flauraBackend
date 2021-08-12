import os
from bson.json_util import dumps
from dotenv import load_dotenv
#from flask import jsonify
import pymongo

load_dotenv() # use dotenv to hide sensitive credential as environment variables
DATABASE_URL=f'mongodb+srv://{os.environ.get("dbUser")}:{os.environ.get("dbPasswort")}'\
             '@flask-mongodb-atlas.wicsm.mongodb.net/'\
             'flaura?retryWrites=true&w=majority' # get connection url from environment

client=pymongo.MongoClient(DATABASE_URL) # establish connection with database
mongo_db=client.db # assign database to mongo_db
mongo_db.launches.drop() # clear the collection

mydb = client.flaura
mycol = mydb.plants


def getPlantByName(name):
    cursor = mycol.find(name)
    list_cur = list(cursor)
    plant = dumps(list_cur)
    return plant

def getAllPlants():
    cursor = mycol.find()
    list_cur = list(cursor)
    plantList = dumps(list_cur)
    return plantList

def setNewPlant(name, waterAmount, critMoist, sleepTime):
    newPlant = {"name": name, "waterAmount": waterAmount, "crtiMoist": critMoist, "sleepTime": sleepTime}
    mycol.insert_one(newPlant)


#function Get List of Plants that contain <name>
#function Get All Plants??
#function Add new Plant to DB
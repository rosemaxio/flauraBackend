import os
from bson.json_util import dumps
from dotenv import load_dotenv
# from flask import jsonify
import pymongo

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
DATABASE_URL = f'mongodb+srv://{os.environ.get("user")}:{os.environ.get("passwort")}' \
               '@flask-mongodb-atlas.wicsm.mongodb.net/' \
               'flaura?retryWrites=true&w=majority'  # get connection url from environment

client = pymongo.MongoClient(DATABASE_URL)  # establish connection with database

# app.config['MONGO_DBNAME'] = 'restdb'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'
# mongo = PyMongo(app)

mydb = client.flaura
mycol = mydb.plants


def getPlantsByName(name):
    cursor = mycol.find({"name": {"$regex": '.*'+name+'.*', "$options": 'i'}})
    list_cur = list(cursor)
    plants = dumps(list_cur)
    return plants


def getAllPlants():
    cursor = mycol.find()
    list_cur = list(cursor)
    plantList = dumps(list_cur)
    return plantList


def setNewPlant(name, waterAmount, critMoist, sleepTime):
    newPlant = {"name": name, "waterAmmountML": waterAmount, "criticalMoisture": critMoist, "sleepTime": sleepTime}
    mycol.insert_one(newPlant)

# function Get List of Plants that contain <name>
# function Get All Plants??
# function Add new Plant to DB

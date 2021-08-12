from flask import Flask, request, jsonify
from flask.json import dump

from . import db

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def index():
    return "<h2 align=center>Welcome to</h2>\n<h1 align=center>Flaura</h1>"


#test to insert data to the data base
@app.route("/test")
def showTest():
    return db.test()

@app.route("/api/v1/plants/", methods=["GET"])
def getPlantList():
    return db.getAllPlants()


@app.route("/api/v1/plants", methods=["GET"])
def getPlant():
    if 'name' in request.args:
        plantName = int(request.args['name'])
    else:
        return "ERROR: No plant Name provided. Specify a name!"

    # results = mycol.find(plantName)
    return db.getPlantByName(plantName)

# @app.route("/api/v1/newPlant")
#def setNewPlant(name, waterAmount, critMoist, sleepTime)
#   db.setNewPlant(name, waterAmount, critMoist, sleepTime)
#   return

# if __name__ == '__main__':
#    app.run(host='0.0.0.0:5000')

from flask import Flask, request, Response
from . import db, plants


def jsonResponse(data):
    return Response(data, mimetype='application/json')


@plants.route("/")
def index():
    return "<h2 align=center>Welcome to</h2>\n<h1 align=center>Flaura</h1>"


@plants.route('/api/plants/', defaults={'name': ""})
@plants.route('/api/plants/<name>')
def get_plants(name):
    return jsonResponse(db.getPlantsByName(name))


@plants.route("/api/v1/plants", methods=["GET"])
def getPlant():
    if 'name' in request.args:
        plantName = request.args['name']
    else:
        return "ERROR: No plant Name provided. Specify a name!"

    # results = mycol.find(plantName)
    return db.getPlantByName(plantName)


@plants.route("/api/v1/plants/", methods=["GET"])
def getPlantList():
    return db.getAllPlants()

# @plants.route("/api/v1/newPlant")
# def setNewPlant(name, waterAmount, critMoist, sleepTime)
#   db.setNewPlant(name, waterAmount, critMoist, sleepTime)
#   return

# if __name__ == '__main__':
#    plants.run(host='0.0.0.0:5000')

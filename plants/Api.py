from flask import Flask, request, Response
from . import db, plants
from bson.json_util import dumps

import numpy as np
from keras.models import load_model
import simplejpeg
import base64


model = load_model('plants/model/keras_model.h5')


def jsonResponse(data):
    return Response(data, mimetype='application/json')


@plants.route("/")
def index():
    return '<h2 align=center>Welcome to</h2>\n<h1 align=center>Flaura</h1><br/><br/><button onclick="alert(\'Deine Mudda\')">Test</button><script>document.addEventListener("message", function (event) {window.ReactNativeWebView.postMessage(event.data);}, false);</script>'


@plants.route('/api/plants/', defaults={'name': ""})
@plants.route('/api/plants/<name>')
def get_plants(name):
    return jsonResponse(db.getPlantsByName(name))

def predict(base64String):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    bytes = base64.standard_b64decode(base64String)
    #image = simplejpeg.decode_jpeg(bytes(base64String, "ascii"))
    image = simplejpeg.decode_jpeg(bytes)
    normalized_image_array = (image.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    return prediction


@plants.route("/search", methods=["POST"])
def searchPlant():
    prediction = predict(request.json["base64"])
    #prediction = [[2, 4]]
    max = (0, 0)
    # get the index of the highest value
    for index, probability in enumerate(prediction[0]):
        if probability > max[1]:
            max = (index, probability)
    # read the line from the before said index
    with open('plants/model/labels.txt', 'r') as label:
        line = label.readlines()
        plant = line[max[0]].rstrip()

    data = dumps({'result': plant[2:]})
    return jsonResponse(data)

# @plants.route("/api/v1/newPlant")
# def setNewPlant(name, waterAmount, critMoist, sleepTime)
#   db.setNewPlant(name, waterAmount, critMoist, sleepTime)
#   return

# if __name__ == '__main__':
#    plants.run(host='0.0.0.0:5000')

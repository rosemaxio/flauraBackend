from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hello, World!</h1>"

@app.route("/api/v1/plant", method=["GET"])
def getPlant():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "ERROR: No ID field provided. Specify an ID!"

    results = [42]

#    for plant in plants:
 #       if plant['id'] == id:
  #          results.append(plant)

    return jsonify(results)

# def app(environment, startResponse):
#    data = (b"No data here\n")
#    status = "200 OK"
#    responseHeaders = [
#        ('Content-type', 'text/plain'),
#        ('Content-Length', str(len(data)))
#    ]
#    startResponse(status, responseHeaders)
#    return iter([data])

# if __name__ == '__main__':
#    app.run(host='0.0.0.0:5000')

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello, World!</h1>"
def app(environment, startResponse):
    data = (b"No data here\n")
    status = "200 OK"
    responseHeaders = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    startResponse(status, responseHeaders)
    return iter([data])

if __name__ == '__main__':
    app.run(host='0.0.0.0:5000')

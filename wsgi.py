from flask import Flask
from plants import plants
from users import users
from test import test

app = Flask(__name__)
app.register_blueprint(plants)
app.register_blueprint(users)
app.register_blueprint(test)
app.run(debug=True)

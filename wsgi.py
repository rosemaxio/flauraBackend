from flask import Flask
from plants import plants
from users import users

app = Flask(__name__)
app.register_blueprint(plants)
app.register_blueprint(users)
app.run(debug=True)

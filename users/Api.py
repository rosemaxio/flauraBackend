import random

from . import users
from flask import request
import json
##### Hier kommt code, den ich einfach von Tina so übernommen habe. Wenn er schlecht ist ist Tina schuld ############
import os
from bson.json_util import dumps
from dotenv import load_dotenv
from flask import jsonify, Response
import pymongo
import hashlib # Die brauchen wir für die Passwörter
import string

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
DATABASE_URL = f'mongodb+srv://{os.environ.get("dbUser")}:{os.environ.get("dbPasswort")}' \
               '@flask-mongodb-atlas.wicsm.mongodb.net/' \
               'flaura?retryWrites=true&w=majority'  # get connection url from environment

client = pymongo.MongoClient(DATABASE_URL)  # establish connection with database

# plants.config['MONGO_DBNAME'] = 'restdb'
# plants.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'
# mongo = PyMongo(plants)

mydb = client.flaura
mycol = mydb.users

def jsonResponse(data):
    return Response(data, mimetype='application/json')
##################### Ende des Codes, den ich einfach nur von Tina übernommen habe #######################
###### Dokumentation der Daten für Login
###### E-Mail: userelement["email"]
###### Passwort: userelement["pwsha256"] <- Dieses Feld soll einen SHA256-Hash von dem Passwort enthalten, dieser ist gesaltet mit "TUCLAB21"
pwsalt = "TUCLAB21"




def getAllUsers():
    cursor = mycol.find({})
    list_cur = list(cursor)
    ppl = dumps(list_cur)
    return ppl

def generatePWhash(password):
    zuhashen = password + pwsalt
    return hashlib.sha256(zuhashen.encode('utf-8')).hexdigest()

def generateToken(length=32):
    # Nach https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

@users.route('/users')
def usersA():
    return jsonResponse(getAllUsers())

@users.route('/users/loginForm')
def loginForm():
    return '<center>Ja Moin. Dann log dich mal ne Runde ein!<br><br><form method="post" action="/users/api/getUser">Token: <input type="text" name="token"><br>Passwort: <input type="password" name="pw"><br><br><input type="submit" value="Abschicken"></form> </center>'
    # Diese Seite funktioniert nicht mehr, seit wir in der API-Funktion einen anderen Typ erwarten

@users.route('/users/api/loginRequest', methods=["POST"])
def attemptLogin():
    bestesAntwortDict = {}
    susUser = mycol.find_one({"email": request.form["username"]})
    ## ToDo: Was machen wir, wenn es diesen User gar nicht gibt? Was kommt dann als Antowort zurück? Niemand weiß es...
    # Gucke, ob das was wir gesendet bekommen haben nachdem es durch die Funktion gejagt wurde mit dem übereinstimmt was bei uns in der DB steht
    if (generatePWhash(request.json["pw"]) == susUser["pwsha256"]):
        bestesAntwortDict["msg"] = "Login erfolgreich"
        ## Wir generieren uns einen Token, mit dem man sich dann später identifizieren kann
        newtoken = generateToken()
        if "tokens" in susUser.keys():
            susUser["tokens"].append(newtoken)
        else:
            susUser["tokens"] = [newtoken]
        mycol.save(susUser)
        bestesAntwortDict["token"] = newtoken
        bestesAntwortDict["loginSuccessful"] = True
    else:
        bestesAntwortDict["msg"] = "Login nicht erfolgreich"
        bestesAntwortDict["loginSuccessful"] = False
    return json.dumps(bestesAntwortDict)

@users.route('/users/api/getUser', methods=["POST"])
def getUserInfobyToken():
    # Diese Funktion will einen token im POST-Header haben, und wenn es ein echter ist, kommt das entsprechende User-Objekt zurück
    bestesAntwortDict = {}
    susUser = mycol.find_one({"tokens": request.form["token"]})
    if susUser == None:
        # Wenn nach dieser Suchaktion susUser None ist, dann war das kein richtiger Token!
        bestesAntwortDict["msg"] = "Incorrect token"
        bestesAntwortDict["error"] = True
        return jsonResponse(json.dumps(bestesAntwortDict))
    else:
        return jsonResponse(str(susUser))


#### Ab hier kommen Testfunktionen, die entfernt werden sollten, sobald das Testen fertig ist

@users.route('/users/api/insertFakeUser')
def genFakeUser():
    ### Denkt sich einen Nutzer aus und fügt ihn in die DB ein
    newuser = {"name": "Alfred Nils Onym", "email": "a.n.onym@protonmail.com","pwsha256":"f98517e61fe651c6c5ce953fcb57c25b4913ee74beea2c1b36d0e19660e61491", "pots": []}
    post_id = mycol.insert_one(newuser).inserted_id
    return str(post_id)

@users.route('/users/api/tests/gethash/<besterstring>')
def testHash(besterstring):
    zuhashen = besterstring + pwsalt
    return hashlib.sha256(zuhashen.encode('utf-8')).hexdigest()


@users.route('/users/api/tests/gettoken')
def testToken():
    return generateToken()
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

def generateLoginToken(length=32):
    # Nach https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

def generatePotToken(length=10):
    # Nach https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


@users.route('/users')
def usersA():
    return jsonResponse(getAllUsers())

@users.route('/users/loginForm')
def loginForm():
    return '<center>Ja Moin. Dann registrier dich mal ne Runde!<br><br><form method="post" action="/users/api/register">Name: <input type="text" name="name"><br>E-Mail: <input type="email" name="email"><br>E-Mail wiederholen: <input type="email" name="emailconfirm"><br>Passwort: <input type="password" name="password"><br>Passwort wiederholen: <input type="password" name="passwordconfirm"><br><br><input type="submit" value="Abschicken"></form> </center>'
    # Diese Seite funktioniert nicht mehr, seit wir in der API-Funktion einen anderen Typ erwarten

@users.route('/users/api/register', methods=["POST"])
def registerUser():
    ### Diese Funktion möchte einen Namen, zwei E-Mails, zwei Passwörter und trägt den User in die DB ein
    ###                            "name", "email", "emailconfirm", "password", "passwordconfirm"
    bestesAntwortDict = {}
    if (request.json["email"] != request.json["emailconfirm"] or request.json["password"] != request.json["passwordconfirm"]):
        bestesAntwortDict["msg"] = "E-Mail-Adressen oder Passwörter stimmen nicht überein."
        bestesAntwortDict["successful"] = False
        return json.dumps(bestesAntwortDict)
    if (request.json["name"] == ""):
        bestesAntwortDict["msg"] = "Name darf nicht leer sein."
        bestesAntwortDict["successful"] = False
        return json.dumps(bestesAntwortDict)
    iniLoginToken = generateLoginToken()
    newuser = {"name": request.json["name"], "email":  request.json["email"],"pwsha256": generatePWhash(request.json["password"]), "pots": [], "tokens":[iniLoginToken]}
    new_id = mycol.insert_one(newuser).inserted_id
    bestesAntwortDict["successful"] = True
    bestesAntwortDict["initialToken"] = iniLoginToken
    return json.dumps(bestesAntwortDict)


@users.route('/users/api/loginRequest', methods=["POST"])
def attemptLogin():
    bestesAntwortDict = {}
    susUser = mycol.find_one({"email": request.json["username"]})
    ## ToDo: Was machen wir, wenn es diesen User gar nicht gibt? Was kommt dann als Antowort zurück? Niemand weiß es...
    # Gucke, ob das was wir gesendet bekommen haben nachdem es durch die Funktion gejagt wurde mit dem übereinstimmt was bei uns in der DB steht
    if (generatePWhash(request.json["pw"]) == susUser["pwsha256"]):
        bestesAntwortDict["msg"] = "Login erfolgreich"
        ## Wir generieren uns einen Token, mit dem man sich dann später identifizieren kann
        newtoken = generateLoginToken()
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

@users.route('/users/api/logoutRequest', methods=["POST"])
def attemptLogout():
    bestesAntwortDict = {}
    susUser = mycol.find_one({"tokens": request.json["token"]})
    ## ToDo: Was machen wir, wenn es diesen User gar nicht gibt? Was kommt dann als Antowort zurück? Niemand weiß es...
    # Diese Funktion löscht den Login-Token, mit dem sie aufgerufen wurde aus der DB
    if (susUser != None):
        bestesAntwortDict["msg"] = "Logout erfolgreich"
        susUser["tokens"].remove(request.json["token"])
        mycol.save(susUser)
        bestesAntwortDict["logoutSuccessful"] = True
    else:
        bestesAntwortDict["msg"] = "Logout nicht erfolgreich"
        bestesAntwortDict["logoutSuccessful"] = False
    return json.dumps(bestesAntwortDict)



@users.route('/users/api/getUser', methods=["POST"])
def getUserInfobyToken():
    # Diese Funktion will einen token im POST-Header haben, und wenn es ein echter ist, kommt das entsprechende User-Objekt zurück
    bestesAntwortDict = {}
    susUser = mycol.find_one({"tokens": request.json["token"]})
    if susUser == None:
        # Wenn nach dieser Suchaktion susUser None ist, dann war das kein richtiger Token!
        bestesAntwortDict["msg"] = "Incorrect token"
        bestesAntwortDict["error"] = True
        return jsonResponse(json.dumps(bestesAntwortDict))
    else:
        return jsonResponse(str(susUser))

@users.route('/users/api/newPot', methods=["POST"])
def createNewPot():
    # Diese Funktion bekommt einen Login-Token übergeben. Sie denkt sich einen Pot-Token für den neuen Pot aus, erzeugt ihn und fügen ihn hinzu
    bestesAntwortDict = {}
    susUser = mycol.find_one({"tokens": request.json["token"]})
    if susUser == None:
        # Wenn nach dieser Suchaktion susUser None ist, dann war das kein richtiger Token!
        bestesAntwortDict["msg"] = "Incorrect token"
        bestesAntwortDict["error"] = True
        return jsonResponse(json.dumps(bestesAntwortDict))
    else:
        newPot = {}
        newPot["token"] = generatePotToken()
        newPot["sleepTime"] = 1;
        newPot["criticalMoisture"] = 0;
        newPot["waterAmmountML"] = 0;
        susUser["pots"].append(newPot)
        mycol.save(susUser)
        return newPot["token"]

@users.route('/users/api/deletePot', methods=["POST"])
def deletePot():
    # Diese Funktion bekommt einen Login-Token und einen Pot-Token übergeben. Sie löscht den Pot mit diesem Token
    bestesAntwortDict = {}
    susUser = mycol.find_one({"tokens": request.json["LoginToken"]})
    if susUser == None:
        # Wenn nach dieser Suchaktion susUser None ist, dann war das kein richtiger Token!
        bestesAntwortDict["msg"] = "Incorrect token"
        bestesAntwortDict["error"] = True
        return jsonResponse(json.dumps(bestesAntwortDict))
    else:
        # Gucken, ob dieser User einen Pot mit diesem PotToken hat, und wenn ja diesen Löschen
        wasFoundAndDeleted = False
        for pot in susUser["pots"]:
            if (pot["token"] == request.json["PotToken"]):
                susUser["pots"].remove(pot)
                wasFoundAndDeleted = True
                mycol.save(susUser)
        if not wasFoundAndDeleted:
            bestesAntwortDict["msg"] = "Pot either not existing or not yours"
            bestesAntwortDict["error"] = True
            return jsonResponse(json.dumps(bestesAntwortDict))
        bestesAntwortDict["msg"] = "Pot deleted"
        bestesAntwortDict["error"] = False
        return jsonResponse(json.dumps(bestesAntwortDict))

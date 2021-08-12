from dotenv import load_dotenv
# from flask import jsonify
import pymongo
'''
load_dotenv()  # use dotenv to hide sensitive credential as environment variables
DATABASE_URL = f'mongodb+srv://{os.environ.get("dbUser")}:{os.environ.get("dbPasswort")}' \
               '@flask-mongodb-atlas.wicsm.mongodb.net/' \
               'flaura?retryWrites=true&w=majority'  # get connection url from environment

client = pymongo.MongoClient(DATABASE_URL)  # establish connection with database
'''
# plants.config['MONGO_DBNAME'] = 'restdb'
# plants.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'
# mongo = PyMongo(plants)

mydb = client.flaura
mycol = mydb.users
'''
pipeline = [
    { $filter: {
               input: "$pots",
               as: "item",
               cond: { $eq: [ "$$item.token", "abc" ] }
            }
         }
} }}]

def getTestValue(token):
    testentry = mycol.aggregate()
    return testentry.

/**
 * specifications: The fields to
 *   include or exclude.
 */
{ $project
     pots: {
            $filter: {
               input: "$pots",
               as: "item",
               cond: { $eq: [ "$$item.token", "abc" ] }
            }
         }
}
'''
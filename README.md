# flauraBackend

## local development
### setup
1. make sure you are running python 3 (e.g. python 3.9.6)
2. set up a virtual environment, e.g. in your terminal
   1. `pip install virtualenv`
   2. `virtualenv flauraenv`
   3. ` source flauraenv/bin/activate` for normal shells (fish shell needs a slightly different command)
   4. (to deactivate just run `deactivate`)
3. install the packages `pip install -r requirements.txt`
4. create a new `.env`- file in root (where requirements.txt, wsgi.py, ... lay)
5. copy the database logins from a trusted developer
6. if heroku is not yet deployed via just github, create a heroku account and ask your local developer to add you as a collaborator
- remember to update the requirements.txt regularaliy via `pip freeze -l > requirements.txt`

### starting
```
python wsgi.py
```

## API
### GET `/test/<accessToken>/<method>/<attr>[?value=<newValue>]`
Used by the Arduino Microcontroller on a plant pot to get/update values from the server.
- `<method>` = get
  - gets the value of the field `<attr>` of the pot with the token `<accessToken>`
- `<method>` = update
  - needs query `/<attr>?value=<newValue>`
  - updates the value of the field `<attr>` of the pot with the token `<accessToken>`
    - to `<newValue>` if it is a float
    - to -1 if it is something that cannot be interpreted as float (e.g. String)

Flaws: Right now it is not restricted in what fields (`<attr>`) can be set. So it would be a way to change the
values of a pot even if you are not logged in/the user that pot belongs to. Could be changed if Microcontroller would also need a loginToken that 
the user adds when adding the potToken. (But shouldn't use one that is already in use, because with a logout that token is deleted)

### GET `/api/plants/<searched>` 
Is used for setting default values for a plant for a pot.
- if `<searched>` is empty, all plants are returned
- else all plants that have `<searched>` somewhere in their name (following Regex \*searched\*)

### POST `/api/users/changePot` 
Expects a JSON in the Request Body with following values:
- `token`: a valid User Token
- `potToken`: a Token of one of the Pots of the User
- attributes to be changed. Can be 1, 2 or all 3
  - `sleepTime` Value (int?) between 1 and 200. How many hours should arduino/microcontroller sleep
  - `criticalMoisture` Value (int?) between 0 and 100 (think per cent). When should the plant be watered again.
  - `waterAmountML` Value (int?) between 0 and 700? How much should the plant be watered.

Example Data:
POST /api/users/changePot
Body:
{
    "token": "ASDFGHasjdkjlasd34asd",
    "plantToken": "ASDFG12RTN",
    "sleepTime": 25
}
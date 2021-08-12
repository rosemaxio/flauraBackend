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
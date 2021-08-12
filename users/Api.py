from . import users

@users.route('/users')
def users():
    return '<h1>USERS</h1>'
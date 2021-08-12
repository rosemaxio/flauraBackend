from . import test

@test.route('/test')
def get_test_value():
    return '<h1>USERS</h1>'
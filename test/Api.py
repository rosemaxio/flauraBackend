from . import test

#@test.route('/test/<accessToken>/<method>/<attr>') # plus params ?value=3
@test.route('/test/<accessToken>/<method>/<attr>')
def get_test_value(accessToken, method, attr):
    print(accessToken, method, attr)
    return '42'
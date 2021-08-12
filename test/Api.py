from . import test
from flask import Flask, request, Response

#@test.route('/test/<accessToken>/<method>/<attr>') # plus params ?value=3
@test.route('/test/<accessToken>/<method>/<attr>')
def get_test_value(accessToken, method, attr):
    # print(accessToken, method, attr)
    if method == "get":
        print('\nLESEN\n')
        return '42'
    elif method == "update":
        value = request.args.get('value')
        print('\nSCHREIBEN\n', value, '\n\n')
        return ''
    
    return ''
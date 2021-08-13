from . import test, db
from flask import Flask, request, Response


# @test.route('/test/<accessToken>/<method>/<attr>') # plus params ?value=3
@test.route('/test/<accessToken>/<method>/<attr>', methods=["GET"])
def get_test_value(accessToken, method, attr):
    # print(accessToken, method, attr)
    if method == "get":
        return db.getTestValue(accessToken, attr)
    elif method == "update":
        if 'value' in request.args:
            value = request.args.get('value', type=float, default=-1)
            return db.updateTestValue(accessToken, attr, value)
    return 'Something went wrong... Have you checked if the URL is correct?'

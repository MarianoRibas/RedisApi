from flask import Blueprint, request
from services.services import push_item, verify_token_middleware

routes_push = Blueprint("routes_push",__name__)

@routes_push.before_request
def auth_middleware():
    return verify_token_middleware(request.headers)
    

@routes_push.route("/push", methods = ['POST'])
def push_route():

    hasMsgKey = 'msg' in request.json
    if not hasMsgKey:
        return {'status' : 'Must provide a message' }, 400
    try:
        message = str(request.json['msg'])
        result = push_item(message)
        if result == 'Connection error':
            return {'status' : 'error' , 'message' : result} , 500
        return {'status' : 'ok'} , 201
    except:
        return {'message' : 'Internal error'} , 500
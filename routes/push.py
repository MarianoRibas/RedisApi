from flask import Blueprint, request
from controllers import push_item

routes_push = Blueprint("routes_push",__name__)

@routes_push.route("/push", methods = ['POST'])
def push_route():
    hasMsgKey = 'msg' in request.json
    if not hasMsgKey:
        return 'Invalid Request' , 400
    message = str(request.json['msg'])
    return push_item(message) , 201
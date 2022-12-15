from flask import Blueprint, request
from services.services import queue_count , verify_token_middleware

routes_count = Blueprint("routes_count",__name__)

@routes_count.before_request
def auth_middleware():
    return verify_token_middleware()

@routes_count.route('/count', methods=['POST'])
def count_route():
    try:
        queueCount = queue_count()
        if queueCount == 'Connection error':
            return {'message' : queueCount} , 500
        response = {
                'status' : 'ok',
                'count' : queueCount
            }
        return response , 200
    except:
        return {'message' : 'Internal error'} , 500
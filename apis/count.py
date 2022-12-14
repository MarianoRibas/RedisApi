from flask import Blueprint, request
from services.services import queue_count , verify_token_middleware

routes_count = Blueprint("routes_count",__name__)

@routes_count.before_request
def auth_middleware():
    return verify_token_middleware()

@routes_count.route('/count', methods=['POST'])
def count_route():
    queueCount = queue_count()
    response = {
            'status' : 'ok',
            'count' : queueCount
        }
    return response , 200
from flask import Blueprint, request
from controllers import queue_size , verify_token_middleware

routes_size = Blueprint("routes_size",__name__)

@routes_size.before_request
def auth_middleware():
    verify_token_middleware()

@routes_size.route('/size', methods=['POST'])
def size_route():
    return queue_size()
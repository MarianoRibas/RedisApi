from flask import Blueprint
from services.services import health_check, verify_token_middleware

routes_health_check = Blueprint("routes_health_check",__name__)

@routes_health_check.before_request
def auth_middleware():
    return verify_token_middleware()

@routes_health_check.route('/healthCheck', methods=['POST'])
def health_check_route():
    try:
        health = health_check()
        if health == 'Connection error':
            return {'message': health} , 500
        return {'message' : health} , 200
    except:
        return {'message' : 'Internal error'} , 500
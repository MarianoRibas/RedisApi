from flask import Blueprint
from controllers import health_check, verify_token_middleware

routes_health_check = Blueprint("routes_health_check",__name__)

@routes_health_check.before_request
def auth_middleware():
    verify_token_middleware()

@routes_health_check.route('/healthCheck', methods=['POST'])
def health_check_route():
    health = health_check()
    return health, 200
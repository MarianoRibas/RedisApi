from flask import Blueprint
from controllers import health_check

routes_health_check = Blueprint("routes_health_check",__name__)

@routes_health_check.route('/healthCheck', methods=['POST'])
def health_check_route():
    health = health_check()
    return health, 200
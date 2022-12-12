from flask import Blueprint, request
from controllers import login

routes_auth = Blueprint("routes_auth",__name__)

@routes_auth.route("/login", methods=['POST'])
def login_route():
    return login(request.json)
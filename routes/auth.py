from flask import Blueprint, request
from controllers import login , verify_token

routes_auth = Blueprint("routes_auth",__name__)

@routes_auth.route("/login", methods=['POST'])
def login_route():
    return login(request.json)

@routes_auth.route("/checkToken", methods=['POST'])
def checkToken_route():
    token = request.headers['Authorization'].split(" ")[1]
    return verify_token(token)
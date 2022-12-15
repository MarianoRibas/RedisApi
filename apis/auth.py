from flask import Blueprint, request
from services.services import login, verify_token

routes_auth = Blueprint("routes_auth",__name__)

@routes_auth.route("/login", methods=['POST'])
def login_route():
    if request.json == None:
        return {"message":"Must provide credentials"} , 400
    
    result = login(request.json)
    if 'token' in result:
        return result, 200
    else:
        return result, 401

# @routes_auth.route("/checkToken", methods=['POST'])
# def checkToken_route():
#     token = request.headers['Authorization'].split(" ")[1]
#     return verify_token(token, output = True)
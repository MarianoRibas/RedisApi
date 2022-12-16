from flask import Blueprint, request
from services.services import login, verify_token

routes_auth = Blueprint("routes_auth",__name__)

@routes_auth.route("/login", methods=['POST'])
def login_route():
    print (request.json)
    try:
        if not request.json:
            return { 'message' : 'Must provide credentials' } , 400
        
        result = login(request.json)
        if 'token' in result:
            return result, 200
        else:
            return result, 401
    except:
        return {'message' : 'Login error'} , 500


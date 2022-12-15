from flask import Blueprint, request, jsonify
import json
from services.services import pop_item, verify_token_middleware, verify_token

routes_pop = Blueprint("routes_pop",__name__)

@routes_pop.before_request
def auth_middleware():
    return verify_token_middleware()
    # hasToken = 'Authorization' in request.headers
    # print(hasToken)
    # if hasToken == False:
    #     return 'Must Provide a Token!' , 401
    # token = request.headers['Authorization'].split(" ")[1]
    # verify_token(token, output=False)

@routes_pop.route("/pop", methods = ['POST'])
def pop_route():
    try:
        popResult = pop_item()
        if not popResult:
            return 'No items to pop' , 400
        
        if popResult == 'Connection error':
            return {'message': popResult} , 500

        response = {
            "status" : "ok",
            "message" : popResult
        }

        return response, 200
    except:
        return {'message' : 'Internal error'} , 500
from flask import Blueprint, request, jsonify
import json
from services.services import pop_item, verify_token_middleware

routes_pop = Blueprint("routes_pop",__name__)

@routes_pop.before_request
def auth_middleware():
    try:
        return verify_token_middleware(request.headers)
    except:
        return 'Authentication Error' , 500

@routes_pop.route("/pop", methods = ['POST'])
def pop_route():
    try:
        popResult = pop_item()
        if not popResult:
            return {'message' : 'No items to pop'} , 200
        
        if popResult == 'Connection error':
            return {'message': popResult} , 500

        response = {
            "status" : "ok",
            "message" : popResult
        }

        return response, 200
    except:
        return {'message' : 'Internal error'} , 500
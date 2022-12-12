from flask import Blueprint, request, jsonify
import json
from controllers import pop_item, verify_token_middleware, verify_token

routes_pop = Blueprint("routes_pop",__name__)

@routes_pop.before_request
def auth_middleware():
    hasToken = 'Authorization' in request.headers
    print(hasToken)
    if hasToken == False:
        return 'Must Provide a Token!' , 401
    token = request.headers['Authorization'].split(" ")[1]
    verify_token(token, output=False)

@routes_pop.route("/pop", methods = ['POST'])
def pop_route():
    poppedItem = pop_item()
    if poppedItem == None:
        return 'No items to pop' , 400
    
    
    stringItem = poppedItem.decode('utf-8')
    

    response = {
        "status" : "ok",
        "message" : stringItem
    }

    return response, 200
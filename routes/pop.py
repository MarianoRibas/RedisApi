from flask import Blueprint, request
from controllers import pop_item, verify_token_middleware

routes_pop = Blueprint("routes_pop",__name__)

@routes_pop.before_request
def auth_middleware():
    verify_token_middleware()

@routes_pop.route("/pop", methods = ['POST'])
def pop_route():
    poppedItem = pop_item()
    if poppedItem == None:
        return 'No items to pop' , 400
    
    return poppedItem, 200
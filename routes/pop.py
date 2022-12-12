from flask import Blueprint, request
from controllers import pop_item

routes_pop = Blueprint("routes_pop",__name__)

@routes_pop.route("/pop", methods = ['POST'])
def pop_route():
    poppedItem = pop_item()
    if poppedItem == None:
        return 'No items to pop' , 400
    
    return poppedItem, 200
from flask import Blueprint
from controllers import queue_size

routes_size = Blueprint("routes_size",__name__)

@routes_size.route('/size', methods=['POST'])
def size_route():
    return queue_size()
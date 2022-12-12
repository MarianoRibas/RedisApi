from flask import Flask, request
import redis
import json
import logging

r = redis.Redis(host='localhost', port=6379)
app = Flask (__name__)

def push_item(item):
    data = {
        'msg' : item
    }
    r.rpush('queue:messages',str(data))
    return "OK"

def pop_item ():
    poppedItem = r.lpop('queue:messages')
    return poppedItem

def queue_size():
    return str(r.llen('queue:messages'))

def health_check():
    health = r.ping()
    print(health)
    if  not health:
        return 'Redis database is unhealthy'
    return 'Redis database is healthy'


@app.route('/api/queue/push', methods=['POST'])
def push_route():
    hasMsgKey = 'msg' in request.json
    if not hasMsgKey:
        return 'Invalid Request' , 400
    message = str(request.json['msg'])
    return push_item(message) , 201

@app.route('/api/queue/pop', methods=['POST'])
def pop_route():
    poppedItem = pop_item()
    if poppedItem == None:
        return 'No items to pop' , 400
    
    return poppedItem, 200

@app.route('/api/queue/size', methods=['POST'])
def size_route():
    return queue_size()

@app.route('/healthCheck', methods=['POST'])
def health_check_route():
    health = health_check()
    return health, 200


if __name__ == '__main__':
    app.run(debug=True)
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
    return str(poppedItem)

def queue_size():
    return str(r.llen('queue:messages'))



@app.route('/api/queue/push', methods=['POST'])
def push_route():
    body = json.dumps(request.form)
    return push_item(body.msg)

@app.route('/api/queue/pop')
def pop_route():

    return pop_item()

@app.route('/api/queue/size')
def size_route():

    return queue_size()

@app.route('/demo', methods=['POST'])
def demo ():
    
    return request.form


if __name__ == '__main__':
    app.run(debug=True)
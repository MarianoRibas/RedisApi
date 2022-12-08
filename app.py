from flask import Flask, request
import redis
import json

r = redis.Redis(host='localhost', port=6379)
app = Flask (__name__)

def push_item(item):
    data = {
        'msg' : item
    }
    r.rpush('queue:messages','Hola')
    return "OK"

def pop_item ():
    poppedItem = r.lpop('queue:messages')
    return str(poppedItem)

def queue_size():
    return str(r.llen('queue:messages'))



@app.route('/api/queue/push')
def push_route():

    return push_item('HOLA')

@app.route('/api/queue/pop')
def pop_route():

    return pop_item()

@app.route('/api/queue/size')
def size_route():

    return queue_size()


if __name__ == '__main__':
    app.run(debug=True)
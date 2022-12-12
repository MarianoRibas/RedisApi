from flask import jsonify
import redis
import jwt
import os
from dotenv import load_dotenv
import datetime


r = redis.Redis(host='localhost', port=6379)
load_dotenv()

secretKey = os.getenv("SECRETKEY")
validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")


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
    if  not health:
        return 'Redis database is unhealthy'
    else:
        return 'Redis database is healthy'



def authenticate(user, password):
    if user == validUsername and password == validPassword:
        return True
    else:
        return False 

def expire_time(mins : int):
    return datetime.datetime.utcnow() + datetime.timedelta(minutes=mins)


def login (credentials):
    hasUsername = 'user' in credentials
    hasPassword = 'password' in credentials

    if not hasUsername or not hasPassword:
        return 'Must provide credentials' , 400

    username = credentials['user']
    password = credentials['password']

    if not authenticate(username,password):
        return 'Invalid Credentials' , 401

    user_info = {"user" : username, "exp" : expire_time(5) }
    token = jwt.encode(user_info, secretKey, algorithm='HS256')

    return {'token' : token} , 200

def verify_token (token):
    try:
        return jwt.decode(token,secretKey, algorithms=['HS256']) , 200
    except jwt.DecodeError:
        return {"msg" : "Invalid Token"} , 401
    except jwt.ExpiredSignatureError:
        return jsonify({"msg" : "Expired Token"}) , 401

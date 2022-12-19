from flask import jsonify, request
import jwt
import os
from dotenv import load_dotenv
import datetime

import redis

r = redis.Redis(host='redis', port=6379)

def get_redis():
    return r

load_dotenv()
secretKey = os.getenv("SECRETKEY")
validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")


def push_item(item):
    print('Docker-debug')
    try:
        result = get_redis().rpush('queue:messages',str(item))
        return result
        
    except Exception as error:
        print(error)
        return 'Connection error'


def pop_item():
    try:
        poppedItem = get_redis().lpop('queue:messages')
        if poppedItem:
            return poppedItem.decode()
        return poppedItem
    except:
        return 'Connection error'


def queue_count():
    try:
        queueCount = get_redis().llen('queue:messages')
        return queueCount
    except:
        return 'Connection error'


def health_check():
    try:
        health = get_redis().ping()
        if  not health:
            return 'Redis database is unhealthy'
        else:
            return 'Redis database is healthy'
    except:
        return 'Connection error'



def authenticate(user, password):
    validUsername = os.getenv("USERNAME")
    validPassword = os.getenv("PASSWORD")
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
        return {"message": "Must provide credentials"} 

    username = credentials['user']
    password = credentials['password']

    if not authenticate(username,password):
        return {"message": "Invalid credentials"}

    user_info = {"user" : username, "exp" : expire_time(30) }
    token = jwt.encode(user_info, secretKey, algorithm='HS256')

    return {'token' : token} 



def verify_token (token):
    try:
        jwt.decode(token,secretKey, algorithms=['HS256'])
    except jwt.DecodeError:
        return jsonify({"msg" : "Invalid Token"}) , 401
        
    except jwt.ExpiredSignatureError:
        return jsonify({"msg" : "Expired Token"}) , 401



def verify_token_middleware(headers):
    hasToken = 'Authorization' in headers
    if hasToken == False:
        return {'msg' : 'Must Provide a Token!'} , 401
    token = headers['Authorization'].split(" ")[1]
    return verify_token(token)
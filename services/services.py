from flask import jsonify, request
import jwt
import os
from dotenv import load_dotenv
import datetime
import redis

r = redis.Redis(host='localhost', port=6379)



load_dotenv()
secretKey = os.getenv("SECRETKEY")
validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")


def push_item(item, r = r):
    try:
        result = r.rpush('queue:messages',str(item))
        return result
        
    except:
        return 'Connection error'


def pop_item (r = r):
    try:
        poppedItem = r.lpop('queue:messages')
        return poppedItem
    except:
        return 'Connection error'


def queue_count(r = r):
    try:
        response = {
            'status' : 'ok',
            'count' : r.llen('queue:messages')
        }
        return response
    except:
        'Connection error'


def health_check(r = r):
    try:
        health = r.ping()
        if  not health:
            return 'Redis database is unhealthy'
        else:
            return 'Redis database is healthy'
    except:
        return 'Connection error'



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
        return {"message": "Must provide credentials"} , 400

    username = credentials['user']
    password = credentials['password']

    if not authenticate(username,password):
        return {"message": "Invalid credentials"} , 401

    user_info = {"user" : username, "exp" : expire_time(30) }
    token = jwt.encode(user_info, secretKey, algorithm='HS256')

    return {'token' : token} , 200



def verify_token (token, output = False):
    try:
        if output:
            return jwt.decode(token,secretKey, algorithms=['HS256']) , 200
        jwt.decode(token,secretKey, algorithms=['HS256']) , 200
    except jwt.DecodeError:
        return "Invalid Token" , 401
        
    except jwt.ExpiredSignatureError:
        return jsonify({"msg" : "Expired Token"}) , 401



def verify_token_middleware():
    hasToken = 'Authorization' in request.headers
    print(hasToken)
    if hasToken == False:
        return 'Must Provide a Token!' , 401
    token = request.headers['Authorization'].split(" ")[1]
    print(token)
    return verify_token(token, output=False)
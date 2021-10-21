# this file contains all methods performed on user

from email_validator import validate_email
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import pymongo
from functions import email_, auth
from datetime import datetime, timedelta
from config import db
from jose import jwt
from pymongo.collection import ReturnDocument
from bson import ObjectId
from templates import webhook_template

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = db.db

def create_user(request):
    if len(request.password) <= 6:
        raise HTTPException(status_code=400, detail={
            "error": "Password length should be more than 6 characters"
        })
    validate_email(request.email)
    request.password = pwd_context.hash(request.password)
    webhook_template.send_user_webhook("Created", request.username)
    email_.send_welcome_message(request.username, request.email)
    user = db.user.insert_one({
        "username": request.username,
        "email": request.email,
        "password": request.password,
        "admin": False,
        "score": 0,
        "createdAt": datetime.now(),
        "friends":[]
    })
    return request


def login_user(form_data):
    user = db.user.find_one({
        "email": form_data.username
    })

    if not user:
        raise HTTPException(status_code=404, detail={
            "error": "User not found"
        })

    verifyPassword = pwd_context.verify(form_data.password, user['password'])

    if not verifyPassword:
        raise HTTPException(status_code=400, detail={
            "error": "Invalid password"
        })

    expire_time = datetime.utcnow() + timedelta(minutes=10080)
    token = jwt.encode({'email': form_data.username,
                       "exp": expire_time}, auth.SECRET_KEY, algorithm='HS256')

    user["_id"] = str(user["_id"])
    user["access_token"] = token
    return user


def profile(user):
    user["_id"] = str(user["_id"])
    return user


def update(request, User):
    user = {}

    if request.email:
        validate_email(request.email)
        user["email"] = request.email

    if request.username:
        user["username"] = request.username

    if request.password:
        if len(request.password) > 6:
            user["password"] = pwd_context.hash(request.password)
        else:
            raise HTTPException(status_code=400, detail={
            "error": "Password length should be more than 6 characters"
            })
    updated_user = db.user.find_one_and_update({
            "email": User["email"]
        }, {
            "$set": dict(user)
        },
        return_document=ReturnDocument.AFTER)
    updated_user["_id"] = str(updated_user["_id"])
    return updated_user


def delete(User):
    user = db.user.find_one_and_delete({"_id":ObjectId(User["_id"])})
    user["_id"] = str(user["_id"])
    webhook_template.send_user_webhook("Deleted", user["username"])
    return user

def update_password(email, password):
    user = db.user.find_one_and_update({
        "email":email
    }, {
        "$set":{
            "password":pwd_context.hash(password)
        }
    })
    if user is None:
        return {
            "error":"User not found"
        }

    user["_id"] = str(user["_id"])
    return user

def search_friend(User, username):
    users = db.user.find({
        "username":username
    })
    userList = []
    for user in users:
        if(user["_id"] == User["_id"]):
            continue
        user["_id"] = str(user["_id"])
        userList.append(user)
    return userList

def add_friend(User,username):
    user = db.user.find_one({
        "username":username
    })
    if user is None:
        raise HTTPException(status_code=404, detail={
            "error":"User not found"
        })

    if(user["_id"] == User["_id"]):
        raise HTTPException(status_code=401, detail={
            "error":"Cannot add yourself"
        })

    if str(user["_id"]) in User["friends"]:
        raise HTTPException(status_code=401, detail={
            "error":"User already friend"
        })

    User['friends'].append(str(user["_id"]))
    updated_user = db.user.find_one_and_update({
        "_id":User["_id"]
    }, {
        "$set":dict(User)
    },
    return_document=ReturnDocument.AFTER)
    
    user["friends"].append(str(User["_id"]))
    db.user.find_one_and_update({
        "_id":user["_id"]
    },{
        "$set":{
            "friends":user["friends"]
        }
    })

    updated_user["_id"] = str(updated_user["_id"])
    return updated_user

def get_friends(User):
    user_list = []
    for id in User["friends"]:
        user = db.user.find_one({
            "_id":ObjectId(id)
        })
        if user is None:
            continue
        user["_id"] = str(user["_id"])
        user_list.append(user)

    return user_list

def remove_friend(id, User):
    User["friends"].remove(id)
    User = db.user.find_one_and_update({
        "_id":ObjectId(User["_id"])
    }, {
        "$set":{
            "friends":User["friends"]
        }
    },return_document=pymongo.ReturnDocument.AFTER)
    User["_id"] = str(User["_id"])
    return User

def leaderboard(limit):
    leaderboard = db.user.find().sort('score', pymongo.DESCENDING).limit(int(limit))
    leaderboard_list = []

    for user in leaderboard:
        user["_id"] = str(user["_id"])
        leaderboard_list.append(user)

    return leaderboard_list

def update_score(User, score):
    updated_user = db.user.find_one_and_update({
        "_id":User["_id"]
    }, 
    {
        "$set":{
            "score":int(User["score"]) + int(score)
        }
    },
    return_document=ReturnDocument.AFTER)

    updated_user["_id"] = str(updated_user["_id"])
    return updated_user
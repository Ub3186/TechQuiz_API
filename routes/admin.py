from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from config.db import db
from templates import webhook_template
from functions import auth
from models.models import User

app = APIRouter()

@app.get("/admin/users")
async def getAllUsers(admin: User = Depends(auth.get_current_user)):
    """
    Get all users from database
    """
    try:
        if not admin["admin"]:
            return {
                'error':"This route is only for admins"
            }

        users = db.user.find()
        usersList = []
        for user in users:
            user["_id"] = str(user["_id"])
            usersList.append(user)
        return usersList
    except:
        raise HTTPException(status_code=500, detail={
            "error":"Something went wrong"
        })

@app.get("/admin/user/{email}", description="Get specific user by email")
async def getUserByEmail(email, admin: User = Depends(auth.get_current_user)):
    if not admin["admin"]:
        return {
            "error":"This route is only for admins"
        }

    user = db.user.find_one({
        "email":email
    })
    if not user:
        raise HTTPException(status_code=404, detail={
            "error":"User not found"
        })
    user["_id"] = str(user["_id"])
    return user

@app.delete("/admin/user/{email}",description="Delete's an user by it's email")
async def deleteUserByEmail(email, admin: User = Depends(auth.get_current_user)):
    if not admin["admin"]:
        return {
            "error":"This route is only for admins"
        }

    user = db.user.find_one_and_delete({
        "email":email
    })
    if not user:
        raise HTTPException(status_code=404, detail={
            "error":"User not found"
        })
    user["_id"] = str(user["_id"])
    return user

@app.post("/webhook")
async def test_webhook(admin: User = Depends(auth.get_current_user)):
    if not admin["admin"]:
        return {
            "error":"This route is only for admins"
        }
    return webhook_template.send_test_webhook()
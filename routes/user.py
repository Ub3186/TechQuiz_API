#this file contains routes for users

from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException
from pymongo.errors import DuplicateKeyError
from email_validator import EmailNotValidError
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import HTMLResponse
from models.models import User, UpdateUser, UpdatePassword

from methods import user_method
from functions import auth, email_
from templates import webhook_template, reset_password

app = APIRouter()

@app.post("/create")
async def create(request:User):
    '''
    Create's User\n
    Requires data in JSON format

    **Required Field**

    - **Username**\n
    - **Email**\n
    - **Password**

    **Optional Field**

    - **Admin**\n
    - **Score**\n
    - **CreatedAt**\n
    '''
    try:
        return user_method.create_user(request)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail={
            "error":"Email already exists"
        })
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail={
            "error":"Invalid email format"
        })


@app.post("/login")
async def login(form_data:OAuth2PasswordRequestForm = Depends()):
    '''
    Login route

    Require's data in Form Body\n
    - **Email**\n
    - **Password**
    '''
    return user_method.login_user(form_data)

@app.get("/user/me")
async def profile(user: User = Depends(auth.get_current_user)):
    '''
    Shows Data of a logged in user

    *Needs Authorised user*
    '''
    try:
        return user_method.profile(user)
    except:
        webhook_template.send_error_webhook("Profile", e)
        raise HTTPException(status_code=500, detail={
            "error":"Something went wrong!"
        })

@app.patch("/user/me")
async def updateUser(request:UpdateUser, User: User = Depends(auth.get_current_user)):
    '''
    Updates user data

    *Needs Authorised user*

    **Require's data in JSON format (valid updates)**
    - **Username**\n
    - **Email**\n
    - **Password**\n
    '''
    try:
        return user_method.update(request, User)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail={
            "error":"Email already exists"
        })
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail={
            "error":"Invalid email format"
        })
    

@app.delete("/user/me")
async def deleteUser(User: User = Depends(auth.get_current_user)):
    '''
    Deletes user data

    *Needs Authorised user*
    '''
    try:
        return user_method.delete(User)
    except Exception as e:
        webhook_template.send_error_webhook("Delete", e)
        raise HTTPException(status_code=500, detail={
            "error":"Something went wrong!"
        })


@app.get("/user/friend/search")
async def search_friend(username,User: User = Depends(auth.get_current_user)):
    '''
    Search Friend

    *Needs email as a query parameter*
    '''
    return user_method.search_friend(User, username)


@app.patch("/user/friend/add")
async def add_friend(username,User: User = Depends(auth.get_current_user)):
    '''
    Add friend

    *Needs username*
    '''
    return user_method.add_friend(User, username)


@app.get("/user/friend/get")
async def get_friends(User: User = Depends(auth.get_current_user)):
    '''
    Get friends

    *Needs authenticated user*
    '''
    return user_method.get_friends(User)

@app.delete("/user/friend/remove")
async def remove_friend(id, User: User = Depends(auth.get_current_user)):
    '''
    Remove friend

    *Needs authenticated user*
    '''
    return user_method.remove_friend(id , User)

@app.get("/leaderboard")
async def leaderboard(limit = 10):
    '''
    Leaderboard
    '''
    return user_method.leaderboard(limit)


@app.patch("/user/score")
async def update_score(score, User: User = Depends(auth.get_current_user)):
    '''
    Update Score

    *Needs score as a query parameter*
    *Need authenticated user*
    '''
    return user_method.update_score(User, score)

@app.post("/forgetpassword")
async def forgetPassword(email):
    '''
    Forget password

    *Needs email as a query parameter*
    '''

    try:
        '''
        Send email
        '''
        send = email_.send_forget_password_message(email)
        return {
            send.text
        }

    except Exception as e:
        webhook_template.send_error_webhook("Forget Password", e)
        raise HTTPException(status_code=500, detail={
            "error":"Something went wrong"
        })

@app.get("/reset_password/{email}", response_class=HTMLResponse)
async def resetPassword(email):
    return HTMLResponse(content=reset_password.reset_password_html(), status_code=200)


@app.patch("/update_password")
async def updatePassword(request: UpdatePassword):
    user = user_method.update_password(request.email, request.password)
    return user

from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from config import db

db = db.db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = '7cda1274f0d16a691b4416be30f757d1628c20ee520f1dbf43865b213f5b335c'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("email")
        if name is None:
            raise credentials_exception
        findUser = db.user.find_one({
            "email":name
        })
        if not findUser:
            raise HTTPException(status_code=404, detail={
                "error":"User not found"
            })
        findUser["_id"] = findUser["_id"]
        return findUser
    except JWTError:
        raise credentials_exception

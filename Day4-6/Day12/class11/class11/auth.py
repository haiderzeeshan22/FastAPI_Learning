from passlib.context import CryptContext
from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta

from db import get_session
from Models import User


SECRET_KEY = "af0bcff3bb29703f0beb5545a7c132e58dda58f0d86df02d15b72baa223111a6"
ALGORITHM = "HS256"
EXP_TIME = 15



pwd_context = CryptContext(schemes="bcrypt")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)




def get_user_from_db(session:Annotated[Session, Depends(get_session)], username:str|None=None, email:str|None= None):
    username = session.exec(select(User).where(User.username == username)).first()
    if not username:
        email = session.exec(select(User).where(User.email == email)).first()
        if email :
            return email
    return username

def authenticate_user(username:str, password:str, session:Annotated[Session, Depends(get_session)]):
    authenticating_user = get_user_from_db(session=session, username=username)
    if not authenticating_user:
        return False
    if not verify_password(password, authenticating_user.password):
        return False
    return authenticating_user


def create_access_token(data:dict, time_delta:timedelta|None):
    data_to_encode = data.copy()
    if time_delta:
        expire = datetime.now(timezone.utc) + time_delta
    else:
        expire= datetime.now(timezone.utc) + timedelta(minutes=EXP_TIME)
    data_to_encode.update({"exp":expire})
    jwt_encode = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)
    return jwt_encode
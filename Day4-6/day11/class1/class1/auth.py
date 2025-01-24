from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from db import get_session
from models import User, TokenData
from datetime import timedelta, timezone, datetime


SECRET_KEY = "26cf297a05473c81e8eef76b565f7c7a427814202087712df686154ec98ed342"
ALGORITHM = "HS256"
TIME_TO_EXPIRE = 15

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes="bcrypt")

def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)



def get_user_from_db(session:Annotated[Session, Depends(get_session)], username:str|None = None, email:str|None=None):
    username = session.exec(select(User).where(User.username == username)).first()
    if not username:
        email = session.exec(select(User).where(User.email == email)).first()
        if email:
            return email
    return username


def authenticate_user(session:Annotated[Session, Depends(get_session)], username:str, password):
    db_user = get_user_from_db(session=session, username=username)
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user


def create_access_token(data:dict, time_delta:timedelta|None):
    data_to_encode = data.copy()
    if time_delta:
        expire = datetime.now(timezone.utc) + time_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes= 15)
    data_to_encode.update({"exp":expire})
    jwt_encode = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encode

def current_user(token:Annotated[str, Depends(oauth_scheme)], session:Annotated[Session, Depends(get_session)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= "invalid Token, please login again",
        headers={"www-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username : str | None = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username= username)
    except:
        raise JWTError
    user = get_user_from_db(session, username=token_data.username)
    if not user:
        raise credential_exception
    return user




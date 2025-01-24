from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, status,Depends
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

from db import get_session
from sqlmodel import Session, select
from typing import Annotated
from models import  TokenData, User


SECRET_KEY = "8da748ca15b9802dd460b79eadc17e11bae3a752fc3c4a586bb4d8130025024b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 15

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)

# def hash_password(password):
#     return pwd_context.hash(password)

# def verify_password(password, hash_password):
#     return pwd_context.verify(password, hash_password)

# def get_user_from_db(session:Annotated[Session, Depends(get_session)],username:str |None=None,  email:str|None=None):
#     # this function will search username and database in the database    
#     username = session.exec(select(User).where(User.username == username)).first()
#     if not username:
#         email = session.exec(select(User).where(User.email == email)).first()
#         return email
#     return username
   

# def authenticate_user(
#         username:str,
#         password:str,
#         session:Annotated[Session, Depends(get_session)]
# ):
#     db_user = get_user_from_db(session=session, username=username)
#     print(f"authenticating User {db_user}")
#     if not db_user:
#         return False
#     if not verify_password(password, db_user.password):
#         return False
#     return db_user
# we create the below function to check whether the password and username provided by user are correct or not / the password provided by user is either associated with the username or not


# to create access token we will use python-jose JWT tokens
# def create_access_token():
#     data_to_encode = data.copy()  # main.py file k ander token k endpoint k ander login k function mai jo access_token ka variable hai jis mai create_access_token ka function store hai odher sy data(username and password) copy kery ga
#     if expiry_time:
#         expire = datetime.now(timezone.utc) + expiry_time
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     data_to_encode.update({"exp":expire})
#     encoded_data = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_data

#we will create the below function for token validation for the user saying whether the token is of current user or not.

# def current_user(token:Annotated[str, Depends(oauth2_scheme)], 
#                  session:Annotated[Session,Depends(get_session)]):
    
#     credential_exeption = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token, Please Login again",headers={"www-authenticate":"Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
#         username : str | None = payload.get("sub") # we are verifying whether the token exist as well or not  and token should be in string form and without username could also be generated that's why typed to None
        
#         if username is None: # if no username in DB
#             raise credential_exeption   
#         token_data = TokenData(username = username)

#     except JWTError:
#         raise credential_exeption
#     user = get_user_from_db(session, username=token_data.username)
#     if not user:
#         raise credential_exeption
#     return user




def get_user_from_db(session:Annotated[Session, Depends(get_session)],
                     username:str|None=None,
                      email : str |None = None ):
    username = session.exec(select(User).where(User.username == username)).first()
    if not username:
        email = session.exec(select(User).where(User.email == email)).first()
        return email
    return username



def authenticate_user(username,
                      password,
                      session:Annotated[Session,Depends(get_session)]):
    db_user = get_user_from_db(session, username= username)
    if not db_user:
        # return {"message":f"user with {username} does not exist in the Database"}
        return False
    if not verify_password(password, hash_password=db_user.password):
        # return {"message":f"dear user {username} your password is incorrect please provide the valid one"}
        return False
    return db_user

                                                    # incase if we don't provide time so that's why we use None
def create_access_token(data:dict, expiry_time:timedelta|None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt

#this current_user function will verify the token of the user 
def current_user(token:Annotated[str, Depends(oauth2_scheme)], 
                 session:Annotated[Session, Depends(get_session)]):
    credentail_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"invalid Token, please login again"},
        headers={"www-authentication":"Bearer"}
    )
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    username : str| None = payload.get("sub")

    if username is None:
        raise credentail_exception
    token_data = TokenData(username=username)

    user = get_user_from_db(session, username=token_data.username)
    if not user:
        raise credentail_exception
    return user

#=================================================================================================================


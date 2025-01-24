from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlmodel import Session


from Models import Register_User, User
from auth import get_user_from_db, hash_password
from db import get_session

api_router = APIRouter(
    prefix="/user",
    tags=["user"],  

)

@api_router.get("/")
async def home():
    return{"message":"APIRouter page"}



@api_router.post("/Add User")
async def create_User(new_user:Annotated[Register_User, Depends()], session:Annotated[Session, Depends(get_session)]):
    db_user = get_user_from_db(session, new_user.username, new_user.email )
    if db_user :
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f"user with name {new_user.username} and email {new_user.email} already exist")
    user = User(username=new_user.username,
                email=new_user.email,
                password=hash_password(new_user.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message":f"User with username {new_user.username} has been added to DataBase successfully"}


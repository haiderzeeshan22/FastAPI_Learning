from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from sqlmodel import Session, select
from models import Register_user, User
from auth import  get_user_from_db, hash_password, current_user
from db import get_session



# we have to add this router in app as well of main.py file 
# APIRouter is a utility class of fastapi, and if we want to route some other api then we use APIRouter
user_router = APIRouter(
    prefix= "/user",
    tags= ["user"],
    responses= {404:{"description" :"Not Found"}}
)


# @user_router.post("/register")
# async def register_user(new_user:Annotated[Register_user, Depends()], session:Annotated[Session, Depends(get_session)]):
#     db_user = get_user_from_db(session, username= new_user.username, email= new_user.email)
#     if db_user:
#         raise HTTPException(status_code=409, detail= f"User {new_user.username} with email {new_user.email} is already existed")
#     user = User(username= new_user.username, email= new_user.email, password= hash_password(new_user.password))
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

# @user_router.get("/me")
# async def user_profile(current_user:Annotated[User, Depends(current_user)]):
#     return current_user

@user_router.get("/user")
async def get_user(session:Annotated[Session, Depends(get_session)]):
    users = session.exec(select(User)).all()
    return users



@user_router.post("/register")
async def register_user(new_user :Annotated[Register_user, Depends()],
                        session:Annotated[Session, Depends(get_session)]):
    db_user = get_user_from_db(session, new_user.username, new_user.email)
    if db_user:
        raise HTTPException(status_code=404, detail=f"User {new_user.username} has already exist in the Database Kindly try new username")
    user = User(username=new_user.username, email=new_user.email, password=hash_password(new_user.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message":f"User {new_user.username} has been added to DB successfully"}

@user_router.get("/me")
async def read_router(current_user:Annotated[User, Depends(current_user)]):
    return current_user

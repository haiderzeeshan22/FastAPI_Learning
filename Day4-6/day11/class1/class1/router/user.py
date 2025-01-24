
from sqlmodel import SQLModel, Session
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from db import get_session
from auth import get_user_from_db, hash_password, current_user
from models import Register_User, User

router : APIRouter = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)


@router.get("/router")
async def check_router():
    return{"message":"welcome this is user router"}

@router.post("/register")
async def register_user(new_user:Annotated[Register_User, Depends()], session:Annotated[Session, Depends(get_session)]):
    db_user = get_user_from_db(session, new_user.username, new_user.email)
    if db_user:
        raise HTTPException(status_code=409, detail=f"user {new_user.username} with email {new_user.email} is already exist")
    user = User(username= new_user.username, 
                email=new_user.email, 
                password=hash_password(new_user.password)
                )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f""" User with name {user.username} successfully registered """}


@router.get("/me")
def user_profile(current_user:Annotated[str, Depends(current_user)]):
    return current_user
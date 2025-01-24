from datetime import timedelta
from fastapi import FastAPI, Depends, status, HTTPException
from sqlmodel import select, Session
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from db import create_tables_and_db, get_session
from Models import Todo, Todo_edit, TokenData
from router.user import api_router
from auth import authenticate_user, EXP_TIME,create_access_token


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating talbes")
    create_tables_and_db()
    print("tables has been Created")
    yield


app : FastAPI= FastAPI(lifespan=lifespan)
app.include_router(router=api_router)


@app.post("/token", response_model=TokenData)
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], 
                session:Annotated[Session, Depends(get_session)]):
    auth_user = authenticate_user(username=form_data.username, password=form_data.password, session=session)
    if not auth_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or Password")
    expire = timedelta(minutes=EXP_TIME)
    access_token = create_access_token({"sub":form_data.username}, expire)

    return TokenData(access_token=access_token, token_type="bearer")




@app.post("/todo")
async def create_todo(todo:Todo, session:Annotated[Session, Depends(get_session)]):
    if todo:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Todo found to insert")
    


@app.get("/todos")
async def get_all_todos(session:Annotated[Session, Depends(get_session)]):
    all_todos = session.exec(select(Todo)).all()
    if all_todos:
        return all_todos
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Even single todo doesn't exit")
@app.put("/update/{id}")
async def update_todo(id:int, todo: Todo_edit, session:Annotated[Session, Depends(get_session)]):
    updating_todo = session.exec(select(Todo).where(Todo.id ==id)).first()
    if updating_todo:
        updating_todo.content = todo.content
        updating_todo.is_availble = todo.is_availble
        session.add(updating_todo)
        session.commit()
        session.refresh(updating_todo)
        return updating_todo

@app.get("/todo/{id}")
async def get_single_todo(id: int, session:Annotated[Session,Depends(get_session)]):
    getting_single_todo = session.exec(select(Todo).where(Todo.id ==id)).first()
    if getting_single_todo:
        return getting_single_todo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

@app.delete("/delete/{id}")
async def delete_todo(id:int, session:Annotated[Session, Depends(get_session)]):
    deleting_todo = session.exec(select(Todo).where(Todo.id ==id)).first()
    if deleting_todo:
        session.delete(deleting_todo)
        session.commit()
        return {"message":f"Todo with id {id} has successfully been deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo not with id {id} Not found")
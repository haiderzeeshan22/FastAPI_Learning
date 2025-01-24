from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session  , select
from router.user import router  
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from db import creat_tables_and_db, get_session 
from models import Todo, Token, User, Todo_create, Todo_edit
from auth import authenticate_user, TIME_TO_EXPIRE, create_access_token, current_user


@asynccontextmanager    
async def lifespan(app:FastAPI):
    print("creating tables")
    creat_tables_and_db()
    print("Tables created")
    yield



app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(router=router)

@app.get("/")
async def home():
    return {"message":"welcome to fastapi todo page"}


@app.post("/token", response_model= Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                session:Annotated[Session, Depends(get_session)]):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username or Password")
    
    expire = timedelta(minutes=TIME_TO_EXPIRE)
    access_token = create_access_token({"sub":form_data.username}, expire)

    return Token(access_token=access_token, token_type="bearer")



@app.post("/todo", response_model=Todo)
async def create_todo(todo : Todo_create,
                      current_user:Annotated[User, Depends(current_user)], 
                      session:Annotated[Session, Depends(get_session)]):
    new_todo = Todo(content= todo.content, user_id= current_user.id, is_available= todo.is_available)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo


@app.get("/todos")
async def get_all_todos( current_user:Annotated[User, Depends(current_user)] ,session:Annotated[Session, Depends(get_session)]):
    all_todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    return all_todos




@app.get("/todo/{id}")
async def get_single_todo(id :int, 
                          current_user:Annotated[User, Depends(current_user)],
                          session:Annotated[Session, Depends(get_session)]):
    single_todo = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    matched_todo = next((todo for todo in single_todo if todo.id == id),None)
    if matched_todo:
        return matched_todo
    else:
        raise HTTPException(status_code = 401, detail="Todo Not Found ")
    




@app.put("/todo/{id}")
async def update_todo(id:int, 
                      todo:Todo_edit, 
                      current_user:Annotated[User, Depends(current_user)],
                      session:Annotated[Session, Depends(get_session)]):
    single_user_all_todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    updating_todo = next((todo for todo in single_user_all_todos if todo.id == id),None)
    if updating_todo:
        updating_todo.content = todo.content
        updating_todo.is_available = todo.is_available
        session.add(updating_todo)
        session.commit()
        session.refresh(updating_todo)
        return updating_todo
    




@app.delete("/todo/{id}")
async def delete_todo(id:int, 
                      current_user:Annotated[User, Depends(current_user)],
                      session:Annotated[Session,Depends(get_session)]):
    single_user_all_todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    deleting_todo = next((todo for todo in single_user_all_todos if todo.id ==id),None)
    if deleting_todo:
        session.delete(deleting_todo)
        session.commit()
        return {"Message":f"Todo with {id} has successfully been deleted"}
    else:
        raise HTTPException(status_code= 401, detail=f"Todo with id {id} Not Found")
    


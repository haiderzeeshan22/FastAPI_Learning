from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from jose import JWTError, jwt  
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Annotated
from contextlib import asynccontextmanager


from auth import authenticate_user, get_user_from_db, ACCESS_TOKEN_EXPIRY_MINUTES, create_access_token, current_user
from db import create_table_and_db, get_session
from router.user import user_router
from models import Todo, User, Token, Todo_Create
# from auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRY_MINUTES, current_user

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("creating Tables")
    create_table_and_db()
    print("Tables created")
    yield



app : FastAPI = FastAPI(lifespan=lifespan)

app.include_router(router=user_router)



@app.get("/")
def read_root():
    return {"":"welcome to dailyDo todo app"}


# @app.post("/user", response_model=User)
# def create_user(user : User, session:Annotated[Session, Depends(get_session)]):
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user




# now we want that whenever anyuser gets login we should give/create him a token
# why we create and give access token to user because whenever user logged in then he/she should be allowed to all routes to access for a specific period of time
# access token give us permission to access authorized endpoints 
# access token is a permission pass
# @app.post("/token", response_model=Token)
# async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()], session:Annotated[Session, Depends(get_session)]):
#     # we have to add functionalities of user authentication
#     authenticating_user = authenticate_user(form_data.username, form_data.password, session=session,)
#     if not authenticating_user:
#         raise HTTPException(status_code=500, detail="Invalid username or password")
#     expire = timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
#     access_token = create_access_token({"sub":form_data.username}, expiry_time=expire)
#     return Token(access_token=access_token, token_type="bearer")


@app.post("/token", response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                session:Annotated[Session, Depends(get_session)]):
    authenticating_user = authenticate_user(form_data.username, form_data.password, session)
    if not authenticating_user:
        raise HTTPException(status_code=404, detail=f"Invalid Username or Password")
    
    expire_time = timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    access_token = create_access_token({"sub":form_data.username}, expire_time)
    return Token(access_token=access_token, token_type="bearer")
# @app.post('/token', response_model=Token)
# async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
#                 session:Annotated[Session, Depends(get_session)]):
#     user = authenticate_user (form_data.username, form_data.password, session)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid username or password")
    
#     expire_time = timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
#     access_token = create_access_token({"sub":form_data.username}, expire_time)

#     # refresh_expire_time = timedelta(days=7)
#     # refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)

#     return Token(access_token=access_token, token_type="bearer")


#==================================================================================================================



@app.post("/todo", response_model=Todo)
async def create_todo(
    current_user:Annotated[User, Depends(current_user)],
    todo:Todo_Create, 
    session:Annotated[Session, Depends(get_session)]
):
    new_todo = Todo(content=todo.content, user_id=current_user.id)
    if new_todo:
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)
        return new_todo
    else:
        raise ResponseValidationError({"Message":"User doesn't exist"})

@app.get("/todos", response_model=list[Todo])
async def get_all_todos(
    current_user:Annotated[User, Depends(current_user)],
    session:Annotated[Session, Depends(get_session)]):

    todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()

    return todos


@app.get("/todo/{id}", response_model=Todo)
async def get_single_todo(id:int , user_id : Optional[int] , session:Annotated[Session, Depends(get_session)]):
    a_todo = session.exec(select(Todo).where(Todo.id == id or Todo.user_id == user_id)).first()
    return a_todo


@app.put("/todo/{id}")
async def update_todo(id:int, todo:Todo, session:Annotated[Session, Depends(get_session)]):
    updating_todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if updating_todo:
        updating_todo.id = todo.id
        updating_todo.content = todo.content
        updating_todo.is_compeleted = todo.is_compeleted
        updating_todo.user_id = todo.user_id
        session.add(updating_todo)
        session.commit()
        session.refresh(updating_todo)
        return updating_todo
    else:
        raise HTTPException(status_code=404, detail="Todo Not Found")

@app.delete("/todo/{id}")
async def delete_todo(id :int, session:Annotated[Session,Depends(get_session)]):
    deleting_todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if deleting_todo:
        session.delete(deleting_todo)
        session.commit()
        return {"Message":f"todo with number {id} has successfully been deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"Todo with number {id} Not Found")






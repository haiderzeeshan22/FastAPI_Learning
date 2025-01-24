from sqlmodel import SQLModel, Field, Session, select
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from typing import Annotated

from db import create_table_and_db, get_session



class Todo(SQLModel, table= True):
    id : int | None = Field(default=None, primary_key=True)
    content : str = Field(index=True, min_length=3, max_length=54)
    is_available : bool = Field(default=False)

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating Tables")
    create_table_and_db()
    print("Tables Created")
    yield

app : FastAPI = FastAPI(lifespan=lifespan, title="FastAPI Todo App", version="1.0.0.1")


@app.post("/todo")
async def create_todo(todo:Todo, session:Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todo")
async def get_all_todos(session:Annotated[Session, Depends(get_session)]):
    all_todos= session.exec(select(Todo)).all()
    if all_todos:
        return all_todos
    else:
        raise HTTPException(status_code=404, detail="Not Even a single Todo Found")


@app.get("/todo/{id}")
async def get_single_todo(id : int, session:Annotated[Session, Depends(get_session)]):
    getting_single_todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if getting_single_todo:
        return getting_single_todo
    else:
        raise HTTPException(status_code=404, detail="Sorry the Todo You are searching for is not available")

@app.put("/todo/{id}")
async def updating_todo(id:int, todo:Todo, session:Annotated[Session, Depends(get_session)]):
    existing_todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if existing_todo:
        existing_todo.id = todo.id
        existing_todo.content = todo.content
        existing_todo.is_available = todo.is_available
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return {"Existing Todo Updated":existing_todo}
    else:
        raise HTTPException(status_code=404, detail="Todo For Updating is Not Available")

@app.delete("/todo/{id}")
async def delete_todo(id: int, session:Annotated[Session, Depends(get_session)]):
    deleting_todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if deleting_todo:
        session.delete(deleting_todo)
        session.commit()
        return {"message":"Todo Deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"No number {id} todo Found")

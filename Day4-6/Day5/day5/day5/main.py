from turtle import getscreen
from fastapi import FastAPI, Depends, HTTPException
from fastapi.exception_handlers import http_exception_handler
from database import create_db_and_table, get_session
from sqlmodel import Session, select
from model import Item
from typing import Annotated


app = FastAPI()


@app.get("/")
def read_root():
    return { 
        "message":"welcome to fastapi learning"
    }

@app.on_event("startup")
def table():
    print("creating tables in database")
    create_db_and_table()
    print("In database tables has been created")

@app.post("/items/", response_model=Item)
def create_item(item:Item, session:Annotated[Session, Depends(get_session)]):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/items/", response_model=list[Item])
def read_items(session=Depends(get_session)):
    items = session.exec(select(Item)).all()   # select all the objects of item and execute a session 
    return items  # select all the objects of item and execute a session and return to client 
 
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id:int, session:Session=Depends(get_session)):
    item = session.exec(select(Item).where(Item.id == item_id)).first()
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="The product is not available")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id:int, item:Item, session:Annotated[Session,Depends(get_session)]):
    existing_item = session.exec(select(Item).where(Item.id == item_id)).first()
    if existing_item:
        existing_item.id = item.id
        existing_item.name = item.name
        existing_item.price = item.price
        existing_item.discription = item.discription
        existing_item.tax = item.tax
        existing_item.is_available = item.is_available
        session.add(existing_item)
        session.commit()
        session.refresh(existing_item)
        return existing_item
    else:
        raise HTTPException(status_code=404, detail="No Task Found")
    

@app.delete("/items/{item_id}")
def delete_item(item_id : int, session:Annotated[Session, Depends(get_session)]):
    deleting_item = session.exec(select(Item).where(Item.id == item_id)).first()
    if deleting_item:
        session.delete(deleting_item)
        session.commit()
        return {"Message":"The Item Deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not Found")
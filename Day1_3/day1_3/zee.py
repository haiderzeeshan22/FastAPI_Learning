from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root(message:str)->dict:
    return {"message": message}

# @app.get("/")
# def read_root(message:str)->str:  here this would raise an error because out functions is explicitly to return str but we are returing dict from function
#     return {"message": message}

class Item(BaseModel):
    name : str
    description: str | None = None
    price : int
    tax : float | None = None

@app.post("/item")
def add_item(item:Item)->dict:
    return {
        "item_name": item.name,
        "item_description": item.description,
        "item_price": item.price,
        "item_tax": item.tax
    }


    
def read_item(item_id:int, nameOfItem: str = Query(min_length=2, max_length=15))->dict:
    return {
        "Item_id": item_id,
        "name Of Item": nameOfItem
    }


@app.get("/item/{item_id}")
def read_iteme(item:dict=Depends(read_item))-> dict:
    return item


@app.get("/query")
def read_query(q:str=Query(min_length=3, max_length=54))-> str:
    return q


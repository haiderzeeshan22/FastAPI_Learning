# from fastapi import FastAPI, Depends, Query
# from pydantic import BaseModel

# app = FastAPI()

# def common_querry_parameter(querry:str = None):
#     return {"querry": querry}

# class Item(BaseModel):
#     name: str 
#     description : str | None = None
#     price : int
#     tax : float | None = None

# # @app.get("/")
# # def read_root(message:str):
# #     return {"Message":message}
# @app.get("/")
# def read_root():
#     return {"Message":"Fastapi"}

# @app.post("/items")
# def add_item(item : Item):
#     return {
#         "Item_name": item.name,
#         "Item_discription": item.description,
#         "Item_price": item.price,
#         "Item_tax": item.tax
#     }

# @app.get("/item")
# def read_item(item_id : int, q : str =None):
#     return {"item_id":item_id,"querry":q}

# @app.get("/item_with_dependancy")
# def read_item(common:dict=Depends(common_querry_parameter)):
#     return common

# @app.get("/search")
# def search_query(q:str=Query(None, min_length=3, max_length=50)):
#     return {"q": q}
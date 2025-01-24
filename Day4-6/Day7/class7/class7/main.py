# from fastapi import FastAPI, Depends
# from database import create_table, get_session
# from sqlmodel import Session, select
# from model import Category, Item


# app = FastAPI()


# @app.on_event("startup")
# def startup():
#     create_table()

# @app.post("/categories/", response_model=Category)
# def create_category(category: Category ,session:Session= Depends(get_session)):
#     session.add(category)
#     session.commit()
#     session.refresh(category)
#     return category

# @app.post("/items", response_model=Item)
# def create_item(item: Item, session:Session=Depends(get_session)):
#     session.add(item)
#     session.commit()
#     session.refresh(item)
#     return item

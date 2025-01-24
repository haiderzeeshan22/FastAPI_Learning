from fastapi import FastAPI, Depends, HTTPException
from models import Category, Product
from database import create_table_and_db, get_session
from sqlmodel import Session

app = FastAPI()

@app.on_event("startup")
def create_table():
    create_table_and_db()
    print("Tables created in RelationshipDB database")

@app.post("/category")
def create_category(category: Category,session:Session= Depends(get_session)):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@app.post("/product")
def create_product(product:Product, session:Session= Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# @app.post("/building")
# def create_building(building:Building, session:Session= Depends(get_session)):
#     session.add(building)
#     session.commit()
#     session.refresh(building)
#     return building


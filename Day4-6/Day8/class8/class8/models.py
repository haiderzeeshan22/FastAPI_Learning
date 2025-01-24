from sqlmodel import SQLModel, Session, Field, Relationship
from fastapi import Query
from typing import Optional, List, Union

class Category(SQLModel, table= True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=20)
    products : List["Product"] = Relationship(back_populates="category")
    # buildings :List["Building"] = Relationship(back_populates= 'category' )

class Product(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name: str
    description : str = Field(min_length=5, max_length=50)
    category_id : Optional[int] = Field(default=None, foreign_key="category.id")
    category : Optional[Category] = Relationship(back_populates="products")

# class Building(SQLModel, table= True):
#     id : Optional[int] = Field(default=None, primary_key=True)
#     name : str
#     description :str= Field(max_length=50, min_length=5)
#     category_id : Optional[int] = Field(default=None, foreign_key="category.id")
#     category : Optional[Category] = Relationship(back_populates = "buildings")
    
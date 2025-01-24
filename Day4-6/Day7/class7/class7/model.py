from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Category(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    items : list["Item"] = Relationship(back_populates="category")

class Item(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    category_id : Optional[int] = Field(default=None, foreign_key="category.id")
    category : Optional[Category] = Relationship(back_populates="items")
    
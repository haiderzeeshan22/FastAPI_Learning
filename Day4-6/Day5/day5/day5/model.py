from sqlmodel import SQLModel, Field
from fastapi import  Query
from typing import Optional


class Item(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    name : str
    discription : str | None = None
    price : int 
    tax : float
    is_available : bool = True
    
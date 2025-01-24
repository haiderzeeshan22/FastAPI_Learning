from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form
from typing import Optional





class Todo(SQLModel, table=True):
    id: Optional[int]=Field(default=None, primary_key=True)
    content : str = Field(index=True, min_length=3, max_length=54)
    is_available : bool = Field(default=False)
    user_id : int  = Field(foreign_key="user.id")


class Todo_create(BaseModel):
    content : str = Field(index=True, min_length=3, max_length=54)
    is_available : bool = Field(default=False)

class Todo_edit(BaseModel):
    content : str = Field(index=True, min_length=3, max_length=54)
    is_available : bool = Field(default=False)    

class User(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    username:str
    email : str
    password: str

class Register_User(BaseModel):
    username:Annotated[str, Form()]
    email:Annotated[str, Form()]
    password:Annotated[str, Form()]
    
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username :str
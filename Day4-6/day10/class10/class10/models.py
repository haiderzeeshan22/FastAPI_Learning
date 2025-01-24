from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional, Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form

class Todo(SQLModel, table= True):
    id : Optional[int] = Field (default= None, primary_key= True)
    content : str = Field(index= True, min_length= 5 , max_length=54)
    is_compeleted : bool = Field(default=False)
    user_id :int = Field(foreign_key="user.id")


class User(SQLModel, table=True):
    id : Optional[int] = Field(primary_key=True, default=None)
    username : str 
    email : str
    password : str

                     # the OAuth2PasswordRequestForm is the dependency class  use to collect username and password as form data
class Register_user(BaseModel):
    username :Annotated[
        str,
        Form() # to use this Form() we have to install python-multipart library of python
    ]
    email :Annotated[
        str,
        Form()
    ]
    password :Annotated[
        str,
        Form() 
    ]
    
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username:str

class Todo_Create(BaseModel):
    content:str = Field(index=True, min_length=3, max_length=54)
# class Token(BaseModel):
#     access_token : str
#     token_type : str

# class TokenData(BaseModel):
#     username: str


# class Todo_Create(BaseModel):
#     content : str = Field(index= True, min_length= 5 , max_length=54)

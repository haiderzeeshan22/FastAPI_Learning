from fastapi import FastAPI
from database import create_db_and_database
from model import Items


app = FastAPI()



@app.on_event("startup")
def on_startup():
    create_db_and_database()


@app.get("/")
def read_root():
    return {"message": "Welcome to zishanDB!"}
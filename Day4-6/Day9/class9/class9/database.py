from sqlmodel import SQLModel, create_engine, Session
# from setting import DATABASE_URL
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
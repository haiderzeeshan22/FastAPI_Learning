from sqlmodel import SQLModel, create_engine, Session
from settings import DATABASE_URL
from models import User, Todo


engine = create_engine(DATABASE_URL)

def creat_tables_and_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
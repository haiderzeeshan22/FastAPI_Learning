from sqlmodel import SQLModel, Field, create_engine,  Session

from models import User
from setting import DATABASE_URL


engine = create_engine(DATABASE_URL)

def create_table_and_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
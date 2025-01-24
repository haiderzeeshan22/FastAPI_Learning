
from sqlmodel import create_engine, Session, SQLModel
from model import Category, Item
from setting import DATABASE_URL

engine = create_engine(DATABASE_URL)

def create_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
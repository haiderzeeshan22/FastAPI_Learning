from sqlmodel import SQLModel, create_engine, Session
from settings import DATABASE_URL


engine = create_engine(DATABASE_URL)


def create_tables_and_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

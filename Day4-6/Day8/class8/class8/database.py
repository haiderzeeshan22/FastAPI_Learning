from sqlmodel import SQLModel, create_engine, Session
from setting import DATABASE_URL



engine = create_engine(DATABASE_URL)


def create_table_and_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
    

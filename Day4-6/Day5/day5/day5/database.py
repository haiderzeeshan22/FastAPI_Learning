from sqlmodel import SQLModel ,Session, select, create_engine
from dotenv import load_dotenv
from setting import DATABASE_URL

import os
load_dotenv()

# os.getenv("DATABASE_URL")



engine = create_engine(DATABASE_URL)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
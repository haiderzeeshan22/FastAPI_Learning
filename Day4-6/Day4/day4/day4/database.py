from sqlmodel import SQLModel, Session, select, Field, create_engine
from starlette.datastructures import Secret
from starlette.config import Config
from dotenv import load_dotenv
import os

# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
# print(f"DATABASE_URL: {DATABASE_URL}")


# try: 
#     config = Config(".env")
# except:
#     config = Config()

# DATABASE_URL = config("DATABASE_URL", default=None)

# DATABASE_URL="postgresql://neondb_owner:zt7u5ksNldHP@ep-calm-band-a1ge730d.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
DATABASE_URL="postgresql+psycopg://mm:MM2244@localhost:5432/MMDB"
# DATABASE_URL="postgresql+psycopg://shaan:Shaan2244@localhost:5432/zishanDB"
                         
engine = create_engine(DATABASE_URL)

def create_db_and_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session



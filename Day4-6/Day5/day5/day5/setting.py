from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except:
    confiq = Config()

DATABASE_URL = config("DATABASE_URL")
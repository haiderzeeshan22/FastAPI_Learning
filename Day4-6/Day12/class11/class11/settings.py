from starlette.config import Config

try:
    config = Config(".env")
except():
    config= Config()

DATABASE_URL = config("DATABASE_URL")
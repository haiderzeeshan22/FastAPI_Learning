from starlette.config import Config
# from dotenv import load_dotenv, find_dotenv
# import os

# DATABASE = load_dotenv(find_dotenv())
# DATA = os.getenv("DATABASE_URL")
try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL")

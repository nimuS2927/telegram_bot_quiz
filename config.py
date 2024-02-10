import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")
TOKEN_API = os.getenv("TOKEN_API")
DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")

PROJECT_DIR = os.path.dirname(__file__)
PATH_TO_DIR_DATABASE = os.path.join(PROJECT_DIR, 'database')
PATH_TO_DATABASE = os.path.join(PATH_TO_DIR_DATABASE, DB_NAME)

PATH_TO_LIBRARY = os.path.join(PROJECT_DIR, 'library')
PATH_TO_DIR_FILES = os.path.join(PROJECT_DIR, 'library', 'files')
PATH_TO_DIR_FIXTURES = os.path.join(PROJECT_DIR, 'library', 'fixtures')


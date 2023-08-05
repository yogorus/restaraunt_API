import os

from dotenv.main import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_CACHE_TIME = os.getenv('REDIS_CACHE_TIME')

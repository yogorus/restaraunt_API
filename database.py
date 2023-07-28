import os
from dotenv.main import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
# user = os.getenv("POSTGRES_USER")
# password = os.getenv("POSTGRES_PASSWORD")
# server_name = os.getenv("SERVER_NAME")
# port = os.getenv("DB_PORT")
# service = os.getenv("DB_SERVICE")
# db_name = os.getenv("DB_NAME")
url = os.getenv("DATABASE_URL")

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@ylab_db:5432/db"
SQLALCHEMY_DATABASE_URL = f"{url}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

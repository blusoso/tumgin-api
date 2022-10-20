
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os

load_dotenv(".env")
SQLALCHEMY_DATABASE_URL = os.environ["DB_URL"]
Base = declarative_base()

engine = create_engine(
    os.getenv("DB_URL", SQLALCHEMY_DATABASE_URL)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_USERNAME = os.environ.get("DB_USERNAME", None)
DB_PASSWORD = os.environ.get("DB_PASSWORD", None)
DB_ADDRESS = os.environ.get("DB_ADDRESS", None)  # hostname:port
AUTH_DB_NAME = os.environ.get("AUTH_DB_NAME", None)
if DB_USERNAME and DB_PASSWORD and DB_ADDRESS and AUTH_DB_NAME:
    SQLALCHEMY_DATABASE_URL = f'postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_ADDRESS}/{AUTH_DB_NAME}'
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./gtkm/auth/database/user_db.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL,
                           connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

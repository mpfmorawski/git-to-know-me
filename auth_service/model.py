from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "users"
    login = Column(String, primary_key=True, index=True)
    token = Column(String)
    scope = Column(String)
    token_type = Column(String)

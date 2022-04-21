from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    github_login = Column(String, nullable=True)
    github_token = Column(String, nullable=True)
    gitlab_login = Column(String, nullable=True)
    gitlab_token = Column(String, nullable=True)
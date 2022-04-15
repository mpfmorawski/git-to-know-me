from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    login: str
    token: str
    scope: str
    token_type: str

    class Config:
        orm_mode = True
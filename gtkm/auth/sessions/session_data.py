from pydantic import BaseModel


class SessionData(BaseModel):
    id: str
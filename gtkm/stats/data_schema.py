from pydantic import BaseModel


class BasicUserData(BaseModel):
    name: str
    surname: str
    user_name: str
    stargaze_count: str
    repos_count: str
    forks_count: str

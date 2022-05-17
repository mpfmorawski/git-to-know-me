from pydantic import BaseModel


class BasicUserData(BaseModel):
    name: str
    surname: str
    user_name: str
    avatar_url: str
    stargaze_count: int
    repos_count: int
    forks_count: int
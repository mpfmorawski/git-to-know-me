from pydantic import BaseModel


class User(BaseModel):
    id: str
    github_login: str
    github_token: str
    gitlab_login: str
    gitlab_token: str

    class Config:
        orm_mode = True

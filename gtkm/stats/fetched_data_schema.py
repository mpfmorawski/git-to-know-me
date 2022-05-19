from pydantic import BaseModel
import datetime


class BasicUserData(BaseModel):
    name: str
    surname: str
    user_name: str
    avatar_url: str
    stargaze_count: int
    repos_count: int
    forks_count: int


class RepositoryLanguages(BaseModel):
    repo_name: str
    repo_language: list


class RepositoryStats(BaseModel):
    repo_owner: str
    repository_name: str
    repo_url: str
    stargaze_count: int
    forks_count: int
    watchers_count: int
    contributors_count: int
    last_user_commit: datetime.date

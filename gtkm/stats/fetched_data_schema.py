from pydantic import BaseModel
import datetime
import json


class BasicUserData(BaseModel):
    name: str
    surname: str
    user_name: str
    avatar_url: str
    stargaze_count: int
    repos_count: int
    forks_count: int


class RepositoryStats(BaseModel):
    repo_language_list: list
    repo_language_list_user: list
    repo_owner: str
    repository_name: str
    repo_url: str
    stargaze_count: int
    forks_count: int
    watchers_count: int
    contributors_count: int
    last_user_commit: datetime.date

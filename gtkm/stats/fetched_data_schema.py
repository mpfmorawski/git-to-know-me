from pydantic import BaseModel


class BasicUserData(BaseModel):
    name: str
    surname: str
    user_name: str
    avatar_url: str
    stargaze_count: int
    repos_count: int
    forks_count: int


class RepositoryStats(BaseModel):
    repo_owner: str
    repository_name: str
    repo_url: str
    stargaze_count: int
    forks_count: int
    watchers_count: int
    contributors_count: int
    last_user_commit: int  # ??

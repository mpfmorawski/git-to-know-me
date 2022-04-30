from fastapi import APIRouter, Depends
import json as JSON
from .github_fetcher import get_general_stats_github

stats = APIRouter()


@stats.get("/api/stats/general_user/{user_name}")
def get_general_stats():
    return {"stars": 1, "github_url": "http://github.com/zdzisiek"}

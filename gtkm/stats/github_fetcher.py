from fastapi import APIRouter

github_fetcher = APIRouter()


@github_fetcher.get("/github/stats/general_user")
def get_general_stats():
    return {"stars": 1, "github_url": "http://github.com/zdzisiek"}

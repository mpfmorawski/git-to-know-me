from fastapi import APIRouter

stats = APIRouter()


@stats.get("/api/stats/general_user/")
def get_general_stats():
    return {"stars": 1, "github_url": "http://github.com/zdzisiek"}

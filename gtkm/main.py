from fastapi import FastAPI

from .auth.service_auth import auth
from .stats.stats_aggregator import stats
from .stats.github_fetcher import github_fetcher

app = FastAPI()

app.include_router(auth)
app.include_router(stats)
app.include_router(github_fetcher)

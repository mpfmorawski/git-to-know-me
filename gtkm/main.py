import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .auth.service_auth import auth
from .stats.stats_aggregator import stats
from .stats.github_fetcher import github_fetcher

app = FastAPI()

app.include_router(auth)
app.include_router(stats)
app.include_router(github_fetcher)


@app.get('/')
async def redirect_typer():
    return RedirectResponse("/index.html")


STATIC_DIR = os.path.dirname(__file__) + "/static"
print(STATIC_DIR)
app.mount("/", StaticFiles(directory=STATIC_DIR), name="static")

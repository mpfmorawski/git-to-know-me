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


app.mount("/", StaticFiles(directory="static"), name="static")

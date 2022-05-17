from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from typing import Optional

from .get_stats.fetch import GithubFetchBasicData, GithubFetchLanguageData

from ..stats.fetched_data_schema import BasicUserData

github_fetcher = APIRouter()


@github_fetcher.get("/github/stats/general_user", response_model=BasicUserData)
async def get_general_stats_github(gtkm_cookie: Optional[str] = Cookie(
    None)) -> JSONResponse:
    '''
    User is identify by cookie file.
    '''

    github_fetcher = GithubFetchBasicData(gtkm_cookie)

    return JSONResponse(await github_fetcher.execute_parsing())


@github_fetcher.get("/github/stats/languages", response_model=BasicUserData)
async def get_languages_stats_github(gtkm_cookie: Optional[str] = Cookie(
    None)) -> JSONResponse:
    '''
    User is identify by cookie file.
    '''

    github_fetcher = GithubFetchLanguageData(gtkm_cookie)

    return {
        "TEST": "TEST"
    }  #JSONResponse(await github_fetcher.execute_parsing())


@github_fetcher.get("/github/stats/top_repos", response_model=BasicUserData)
async def get_repos_stats_github(gtkm_cookie: Optional[str] = Cookie(
    None)) -> JSONResponse:
    '''
    User is identify by cookie file.
    '''

    return {
        "TEST": "TEST"
    }  #JSONResponse(await github_fetcher.execute_parsing())

from fastapi import APIRouter
import json as JSON
from ..stats.aggregate_data_schema import BasicUserData
from .get_stats.aggregate import GithubAggregateBasicData

from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from typing import Optional

stats = APIRouter()


@stats.get("/api/stats/general_user")#, response_model=BasicUserData)
async def get_general_stats(gtkm_cookie: Optional[str] = Cookie(
        None)) -> JSONResponse:
    '''
    FOR MVP purpose. Simplified data aggregator; aggregate only Github data.
    '''

    github_aggregator = GithubAggregateBasicData(gtkm_cookie)

    return JSONResponse(await github_aggregator.execute_collecting())

from fastapi import APIRouter, Request
from time import time
import httpx
import asyncio

github_fetcher = APIRouter()

async def task(URL):
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        return response.text

@github_fetcher.get("/github/stats/{user_name}")
async def get_general_stats(git_user: str):
    URL = "https://api.github.com/users/{}".format(git_user)
    return await task(URL)
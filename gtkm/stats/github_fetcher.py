from fastapi import APIRouter
import json as JSON
import httpx

github_fetcher = APIRouter()

URL_BASE = "https://api.github.com"


async def task(URL):
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
    return response.text

def jsons_parser(basic_user_data: str, repos_info: str):
    JSON_basic_user_data = JSON.loads(basic_user_data)
    JSON_repos_info = JSON.loads(repos_info)

    stargaze_count = 0
    forks_count = 0
    for element in JSON_repos_info:
        stargaze_count = stargaze_count+element.get("stargazers_count")
        forks_count = forks_count + element.get("forks_count")

    json_summary_file = {'name': JSON_basic_user_data.get("name").split()[0],
                 'surname': JSON_basic_user_data.get("name").split()[1],
                 'user_name': JSON_basic_user_data.get("login"),
                 'stargaze_count': stargaze_count,
                 'repos_count': len(JSON_repos_info),
                 'forks_count': forks_count}

    return json_summary_file


async def get_basic_info(git_user: str):
    URL_basic_user_data = URL_BASE + "/users/{}".format(git_user)
    basic_user_data = await task(URL_basic_user_data)

    URL_repos_info = URL_BASE + "/users/{}/repos".format(git_user)
    repos_info = await task(URL_repos_info)

    ''' Return parsed user and repos info'''
    return jsons_parser(basic_user_data, repos_info)


@github_fetcher.get("/github/stats/{user_name}")
async def get_general_stats(git_user: str):
    bb = await get_basic_info(git_user)
    return bb

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import JSONResponse
from typing import Optional
import json as JSON
import httpx

from ..stats.fetched_data_schema import BasicUserData
from ..common import gen_url

github_fetcher = APIRouter()

URL_BASE = "https://api.github.com"


async def get_endpoint_data(URL: str, cookie=None):
    if cookie is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
        return response.text
    else:
        cookies = {'gtkm_cookie': cookie}
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, cookies=cookies)
        return response


# Function manage JSON name filed
def extract_name(JSON_basic_user_data: JSON):
    if JSON_basic_user_data.get("name") != None:
        user_name_data = JSON_basic_user_data.get("name")

        if len(user_name_data) == 1:
            user_name = user_name_data
            user_surname = None
        else:
            user_name = user_name_data.split()[0]
            user_surname = user_name_data.split()[1]
    else:
        user_name = None
        user_surname = None

    return user_name, user_surname


def jsons_parser(basic_user_data: str, repos_info: str):
    JSON_basic_user_data = JSON.loads(basic_user_data)
    JSON_repos_info = JSON.loads(repos_info)

    stargaze_count = 0
    forks_count = 0
    for element in JSON_repos_info:
        stargaze_count = stargaze_count + element.get("stargazers_count")
        forks_count = forks_count + element.get("forks_count")

    user_name, user_surname = extract_name(JSON_basic_user_data)
    ''' Fetched and parsed user data '''
    json_summary_file = {
        'name': user_name,
        'surname': user_surname,
        'user_name': JSON_basic_user_data.get("login"),
        'stargaze_count': stargaze_count,
        'repos_count': len(JSON_repos_info),
        'forks_count': forks_count
    }

    return json_summary_file


async def get_user_name(gtkm_cookie):
    if gtkm_cookie:
        user_id = await get_endpoint_data(gen_url('/auth/user/id'),
                                          cookie=gtkm_cookie)

        user_name = await get_endpoint_data(gen_url("/auth/user/?id=" +
                                                    user_id.json()["id"]),
                                            cookie=gtkm_cookie)

        return user_name.json()["github_login"]

    return None


async def get_basic_info(gtkm_cookie):

    git_user = await get_user_name(gtkm_cookie)

    URL_basic_user_data = URL_BASE + f"/users/{git_user}"
    basic_user_data = await get_endpoint_data(URL_basic_user_data)
    ''' Check if user exist, if not return error message '''
    try:
        JSON_temp_user_check = JSON.loads(basic_user_data)
        if JSON_temp_user_check.get("message") == "Not Found":
            return {"Error": "User not found"}
    except:
        pass

    URL_repos_info = URL_BASE + f"/users/{git_user}/repos"
    repos_info = await get_endpoint_data(URL_repos_info)
    ''' Return parsed user and repos info'''
    return jsons_parser(basic_user_data, repos_info)


@github_fetcher.get("/github/stats/general_user", response_model=BasicUserData)
async def get_general_stats_github(gtkm_cookie: Optional[str] = Cookie(
    None)) -> JSONResponse:
    '''
    User is identify by cookie file.
    '''
    return JSONResponse(await get_basic_info(gtkm_cookie))

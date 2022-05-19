import httpx
'''
Simple function for downloading data from passed endpoint address.
Function accept cookie file if necessary.
'''


async def get_endpoint_data(URL: str, cookie=None) -> str:
    if cookie is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
        return response.text
    else:
        cookies = {'gtkm_cookie': cookie}
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, cookies=cookies)
        return response

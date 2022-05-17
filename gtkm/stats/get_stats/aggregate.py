from ...common import gen_url, get_endpoint_data

import json
import os


class GithubAggregateBasicData():

    gtkm_cookie = None

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie

    async def execute_collecting(self):

        if self.gtkm_cookie:
            general_user_data = await get_endpoint_data(
                gen_url('/github/stats/general_user'), cookie=self.gtkm_cookie)

        return general_user_data.json()

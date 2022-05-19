from ...common import gen_url, get_endpoint_data


class GithubAggregateBasicData():

    gtkm_cookie = None

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie

    async def execute_collecting(self):

        if self.gtkm_cookie:
            general_user_data = await get_endpoint_data(
                gen_url('/github/stats/general_user'), cookie=self.gtkm_cookie)

        return general_user_data.json()


class GithubAggregateLanguageData():

    gtkm_cookie = None

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie

    async def execute_collecting(self):

        if self.gtkm_cookie:
            general_user_data = await get_endpoint_data(
                gen_url('/github/stats/languages'), cookie=self.gtkm_cookie)

        return general_user_data.json()


class GithubAggregateTopRepos():

    gtkm_cookie = None

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie

    async def execute_collecting(self):

        if self.gtkm_cookie:
            general_user_data = await get_endpoint_data(
                gen_url('/github/stats/top_repos'), cookie=self.gtkm_cookie)

        return general_user_data.json()

from .aggregation_base_class import AggregationBaseClass

""" Set of classes for data aggregation purpose; in future work, classes will be extended with new functionalities (e.g. downloading data from gitlab) """


class GithubAggregateBasicData(AggregationBaseClass):

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie
        super().__init__()

    async def execute_collecting(self):

        github_general_user_data = await self._execute_collecting_data(
            '/github/stats/general_user')

        return github_general_user_data


class GithubAggregateLanguageData(AggregationBaseClass):

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie
        super().__init__()

    async def execute_collecting(self):

        github_languages_data = await self._execute_collecting_data(
            '/github/stats/languages')

        return github_languages_data


class GithubAggregateTopRepos(AggregationBaseClass):

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie
        super().__init__()

    async def execute_collecting(self):

        github_top_repos_data = await self._execute_collecting_data(
            '/github/stats/top_repos')

        return github_top_repos_data

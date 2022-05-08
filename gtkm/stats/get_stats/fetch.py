from ...common import gen_url, get_endpoint_data

import json
import os


class FetcherBase:
    config = []

    def __init__(self, path: str = None) -> None:
        if path is not None:
            with open(path) as json_file:
                self.config = json.load(json_file)
        else:
            # TODO: Add error expectation handler
            pass


class GithubFetchBasicData(FetcherBase):

    # Fetcher config class
    CONFIG_DIR = os.path.dirname(__file__) + "/config"
    PATH = CONFIG_DIR + "/github_config.json"

    URL_BASE = "https://api.github.com"

    user_data_json_file: json = {}

    gtkm_cookie = None

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie
        super().__init__(self.PATH)

    async def execute_parsing(self):
        user_name = await self._get_user_name()

        for data_part in self.config["basic info"]:
            parsing_data = getattr(self, "_get_" + data_part["function"])

            status = await parsing_data(self.URL_BASE +
                                        str(data_part["URL"]).format(user_name))

        return self.user_data_json_file

    async def _get_user_name(self):
        if self.gtkm_cookie:
            user_id = await get_endpoint_data(gen_url('/auth/user/id'),
                                              cookie=self.gtkm_cookie)

            user_name = await get_endpoint_data(gen_url("/auth/user/?id=" +
                                                        user_id.json()["id"]),
                                                cookie=self.gtkm_cookie)

        return user_name.json()["github_login"]

    # USER BASIC INFO
    async def _get_basic_user_data(self, URL: str = None) -> None:
        basic_user_data = await get_endpoint_data(URL)

        JSON_basic_user_data = json.loads(basic_user_data)

        ''' Check if user exist, if not return error message '''
        if JSON_basic_user_data.get("message") == "Not Found":
            # TODO: Error handler
            pass

        user_name, user_surname = self._extract_name(
            json.loads(basic_user_data))

        self.user_data_json_file['name'] = user_name
        self.user_data_json_file['surname'] = user_surname
        self.user_data_json_file['user_name'] = JSON_basic_user_data.get(
            "login")
        self.user_data_json_file['avatar_url'] = JSON_basic_user_data.get(
            "avatar_url")

        print(self.user_data_json_file)

    # Function manage JSON name filed

    def _extract_name(self, JSON_basic_user_data: json):
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

    # RESPOSITORY BASIC INFO

    async def _get_user_repos_info(self, URL: str = None) -> None:
        repos_info = await get_endpoint_data(URL)
        JSON_repos_info = json.loads(repos_info)

        stargaze_count = 0
        forks_count = 0
        for element in JSON_repos_info:
            stargaze_count = stargaze_count + element.get("stargazers_count")
            forks_count = forks_count + element.get("forks_count")

        self.user_data_json_file['stargaze_count'] = stargaze_count
        self.user_data_json_file['repos_count'] = len(JSON_repos_info)
        self.user_data_json_file['forks_count'] = forks_count

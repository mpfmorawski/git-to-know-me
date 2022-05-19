from ...common import gen_url, get_endpoint_data

import json
import os


class FetcherBase:
    # Fetcher config class
    CONFIG_DIR = os.path.dirname(__file__) + "/config"
    PATH = CONFIG_DIR + "/github_config.json"

    URL_BASE = "https://api.github.com"

    config = []

    def __init__(self, path: str = None) -> None:
        if path is not None:
            with open(path) as json_file:
                self.config = json.load(json_file)
        else:
            # TODO: Add error expectation handler
            pass

    async def execute_parsing_test(self):
        user_name = await self._get_user_name()

        for data_part in self.config["basic info"]:
            parsing_data = getattr(self, "_get_" + data_part["function"])

            status = await parsing_data(
                self.URL_BASE + str(data_part["URL"]).format(user_name))

        return self.user_data_json_file

    async def _get_user_name(self):
        if self.gtkm_cookie:
            user_id = await get_endpoint_data(gen_url('/auth/user/id'),
                                              cookie=self.gtkm_cookie)

            user_name = await get_endpoint_data(gen_url("/auth/user/?id=" +
                                                        user_id.json()["id"]),
                                                cookie=self.gtkm_cookie)

        # TODO: potentially error when user_name doesn't exist
        return user_name.json()["github_login"]

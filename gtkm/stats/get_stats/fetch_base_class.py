from ...common import gen_url, get_endpoint_data

import json
import os
""" Base class for main fetch classes"""


class FetcherBase:
    # Fetcher config class
    CONFIG_DIR = os.path.dirname(__file__) + "/config"
    PATH = CONFIG_DIR + "/github_config.json"

    URL_BASE = "https://api.github.com"

    gtkm_cookie = None

    json_file_to_return: json = {}

    config = []

    def __init__(self, path: str = None) -> None:
        if path is not None:
            with open(path) as json_file:
                self.config = json.load(json_file)
        else:
            # TODO: Add error expectation handler
            pass

    async def _get_user_name(self):
        if self.gtkm_cookie:
            user_id = await get_endpoint_data(gen_url('/auth/user/id'),
                                              cookie=self.gtkm_cookie)

            user_name = await get_endpoint_data(gen_url("/auth/user/?id=" +
                                                        user_id.json()["id"]),
                                                cookie=self.gtkm_cookie)

        # TODO: potentially error when user_name doesn't exist
        return user_name.json()["github_login"]

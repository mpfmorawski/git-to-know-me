from ...common import gen_url, get_endpoint_data
from .fetch_base_class import FetcherBase
from datetime import date

import json
""" Set of classes for data fetching purpose """


class GithubFetchBasicData(FetcherBase):

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie
        super().__init__(self.PATH)

    async def execute_parsing(self) -> str:

        for data_part in self.config["basic info"]:
            parsing_data = getattr(self, "_get_" + data_part["function"])

            # TODO: Check status variable; now is unused!
            status = await parsing_data(
                self.URL_BASE +
                str(data_part["URL"]).format(await self._get_user_name()))

        return self.json_file_to_return

    # User basic info

    async def _get_basic_user_data(self, URL: str = None) -> None:
        basic_user_data = await get_endpoint_data(URL)

        JSON_basic_user_data = json.loads(basic_user_data)
        ''' Check if user exist, if not return error message '''
        if JSON_basic_user_data.get("message") == "Not Found":
            # TODO: Error handler
            pass

        user_name, user_surname = self._extract_name(
            json.loads(basic_user_data))

        self.json_file_to_return['name'] = user_name
        self.json_file_to_return['surname'] = user_surname
        self.json_file_to_return['user_name'] = JSON_basic_user_data.get(
            "login")
        self.json_file_to_return['avatar_url'] = JSON_basic_user_data.get(
            "avatar_url")

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

        self.json_file_to_return['stargaze_count'] = stargaze_count
        self.json_file_to_return['repos_count'] = len(JSON_repos_info)
        self.json_file_to_return['forks_count'] = forks_count


class GithubFetchRepositoryData(FetcherBase):

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie
        super().__init__(self.PATH)

    async def execute_parsing(self) -> str:
        user_name = await self._get_user_name()

        for data_part in self.config["repos info"]:
            parsing_data = getattr(self, "_get_" + data_part["function"])

            status = await parsing_data(
                self.URL_BASE + str(data_part["URL"]).format(user_name))

        return self.json_file_to_return

    async def _get_repos_data_info(self, URL: str = None) -> None:

        users_repositories = await get_endpoint_data(URL)

        JSON_basic_user_data = json.loads(users_repositories)

        temp_final_json = []

        # TODO: Remove counter_MVP_ONLY and choose five best repos intelligently
        counter_MVP_ONLY = 0

        for repository in JSON_basic_user_data:
            temp_json: json = {}

            temp_json["repo_owner"] = repository.get("owner")["login"]
            temp_json["repository_name"] = repository.get("name")
            temp_json["repo_url"] = repository.get("html_url")
            temp_json["stargaze_count"] = repository.get("stargazers_count")
            temp_json["forks_count"] = repository.get("forks_count")
            temp_json["watchers_count"] = repository.get("watchers_count")

            # TODO: In MVP version those data aren't proper and hardcoded!
            temp_json["contributors_count"] = 0
            temp_json["last_user_commit"] = date.fromisoformat(
                repository.get("updated_at")[0:10])

            temp_json["top_5_place"] = 0

            temp_final_json.append(temp_json)

#            counter_MVP_ONLY = counter_MVP_ONLY + 1

#            if counter_MVP_ONLY >= 5:
#                break

#        final_json = self._put_proper_order(temp_final_json)
        num = 1
        for json_file in temp_final_json:
            json_file["top_5_place"] = num
            num = num + 1

        self.json_file_to_return = temp_final_json

    def _put_proper_order(self, json_file_RAW):

        json_file = json_file_RAW

        temp_json = []

        biggest_stargaze_count = 0

        # start place value
        place_counter = 1

        while (len(json_file) > 0):
            biggest_stargaze_count = 0
            temp_json_file_order = []
            for index in range(len(json_file)):
                if json_file[index].get(
                        "stargaze_count") > biggest_stargaze_count:
                    temp_json_file_order = []
                    temp_json_file_order.append(index)
                    biggest_stargaze_count = json_file[index].get(
                        "stargaze_count")

                elif json_file[index].get(
                        "stargaze_count") == biggest_stargaze_count:
                    temp_json_file_order.append(index)

            for index in temp_json_file_order:
                json_file[index]["top_5_place"] = place_counter
                temp_json.append(json_file[index])
                place_counter = place_counter + 1
                json_file.pop(index)

        return temp_json


class GithubFetchLanguageData(FetcherBase):

    def __init__(self, gtkm_cookie):
        self.gtkm_cookie = gtkm_cookie
        super().__init__(self.PATH)

    async def execute_parsing(self) -> str:
        user_name = await self._get_user_name()

        for data_part in self.config["language info"]:
            parsing_data = getattr(self, "_get_" + data_part["function"])

            status = await parsing_data(
                self.URL_BASE + str(data_part["URL"]).format(user_name))

        return self.json_file_to_return

    async def _get_repos_data_language(self, URL: str = None) -> None:
        language_list_URL = "/repos/{}/{}/languages"
        user_name = await self._get_user_name()

        users_repositories = await get_endpoint_data(URL)

        JSON_basic_user_data = json.loads(users_repositories)

        temp_final_json = []

        # TODO: Remove counter_MVP_ONLY and choose five best repos intelligently
        counter_MVP_ONLY = 0

        for repository in JSON_basic_user_data:

            repo_language = json.loads(await get_endpoint_data(
                self.URL_BASE +
                language_list_URL.format(user_name, repository.get("name"))))

            temporary_byte_sum = 0
            temporary_json_data_file_languages = []
            temporary_json_data_file: json = {}

            for rep in repo_language:
                temporary_byte_sum = temporary_byte_sum + \
                    repo_language.get(rep)

            for rep in repo_language:
                json_obj: json = {}
                json_obj = {
                    f"{rep}":
                    f"{float(repo_language.get(rep)/temporary_byte_sum)}"
                }
                temporary_json_data_file_languages.append(json_obj)

            temporary_json_data_file["repo_name"] = repository.get("name")
            temporary_json_data_file[
                "repo_languages"] = temporary_json_data_file_languages

            temp_final_json.append(temporary_json_data_file)

#            counter_MVP_ONLY = counter_MVP_ONLY + 1

#            if counter_MVP_ONLY >= 5:
#                break

        self.json_file_to_return = temp_final_json

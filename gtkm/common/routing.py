from strenum import StrEnum


class Service(StrEnum):
    ENDPOINT = "endpoint"  #endpoint used by user (access to site)
    AUTH = 'auth'
    GITHUB_FETCHER = 'github'
    GITLAB_FETCHER = 'gitlab'
    STATS_AGGREGATOR = 'aggregator'


SERVICE_PORTS = {
    Service.ENDPOINT: 8000,
    Service.AUTH: 8001,
    Service.GITHUB_FETCHER: 8002,
    Service.GITLAB_FETCHER: 8003,
    Service.STATS_AGGREGATOR: 8004
}


def gen_url(endpoint: str) -> str:
    '''Generates full URL from selected API endpoint'''
    return "http://127.0.0.1:8000" + endpoint

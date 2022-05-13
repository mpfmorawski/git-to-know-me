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
    if "api" in endpoint:
        port = "8000"
    elif "auth" in endpoint:
        port = "8001"
    elif "github" in endpoint:
        port = "8002"
    elif "gitlab" in endpoint:
        port = "8003"
    elif "stats" in endpoint:
        port = "8004"
    else:
        port = "8000"
    return f"http://127.0.0.1:{port}{endpoint}"

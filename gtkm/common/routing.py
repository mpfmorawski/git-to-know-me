import re
from strenum import StrEnum
from fastapi.logger import logger


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

REGEX_API_TO_PORT = {
    "(\/)?(api\/)?auth\/.*": SERVICE_PORTS[Service.AUTH],
    "(\/)?(api\/)?github\/.*": SERVICE_PORTS[Service.GITHUB_FETCHER],
    "(\/)?(api\/)?gitlab\/.*": SERVICE_PORTS[Service.GITLAB_FETCHER],
    "(\/)?(api\/)?stats\/.*": SERVICE_PORTS[Service.STATS_AGGREGATOR],
    ".*\.(html|js|css|png|svg|jpg|ttf)$": SERVICE_PORTS[Service.ENDPOINT],
}


def gen_url(endpoint: str) -> str:
    '''Generates full URL from selected API endpoint'''
    port = None
    for pattern, p in REGEX_API_TO_PORT.items():
        if re.fullmatch(pattern, endpoint) is not None:
            port = p
            break
    if port is None:
        port = SERVICE_PORTS[Service.ENDPOINT]
        logger.warning(
            f"Unknown endpoint: {endpoint}, reditecting to: http://127.0.0.1:{port}{endpoint}"
        )
    return f"http://127.0.0.1:{port}{endpoint}"


#TODO handle single service routing

#!/usr/bin/env python3

import uvicorn

from multiprocessing import Process

from fastapi import FastAPI

from gtkm.auth.service_auth import auth
from gtkm.stats.stats_aggregator import stats
from gtkm.stats.github_fetcher import github_fetcher

from gtkm.common.routing import SERVICE_PORTS, Service

auth_app = FastAPI()
auth_app.include_router(auth)

stats_app = FastAPI()
stats_app.include_router(stats)

github_fetch_app = FastAPI()
github_fetch_app.include_router(github_fetcher)

if __name__ == "__main__":
    processes = [
        Process(target=uvicorn.run,
                args=("main_microservices:auth_app", ),
                kwargs={
                    "host": "127.0.0.1",
                    "port": SERVICE_PORTS[Service.AUTH],
                    "log_level": "info"
                }),
        Process(target=uvicorn.run,
                args=("main_microservices:stats_app", ),
                kwargs={
                    "host": "127.0.0.1",
                    "port": SERVICE_PORTS[Service.STATS_AGGREGATOR],
                    "log_level": "info"
                }),
        Process(target=uvicorn.run,
                args=("main_microservices:github_fetch_app", ),
                kwargs={
                    "host": "127.0.0.1",
                    "port": SERVICE_PORTS[Service.GITHUB_FETCHER],
                    "log_level": "info"
                }),
    ]

    for proces in processes:
        proces.start()

    while processes:
        processes.pop().join()
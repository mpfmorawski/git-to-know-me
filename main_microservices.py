#!/usr/bin/env python3
import argparse
import os
import uvicorn

from multiprocessing import Process

from fastapi import FastAPI

os.environ["MULTISERVICE_DEPLOYMENT"] = "1"

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


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        "Launcher for multiservice deployment of gtkm. By default launchess all of services. Recomended to use with nginx at http://127.0.0.1:8000"
    )

    parser.add_argument("-s",
                        "--service",
                        choices=["auth_app", "stats_app", "github_fetch_app"],
                        help="Select single service to launch")
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Select used port (works only when single service is launched).")
    return parser.parse_args()


def run_all():
    processes = [
        Process(target=uvicorn.run,
                args=("main_microservices:auth_app", ),
                kwargs={
                    "host": "127.0.0.1",
                    "port": SERVICE_PORTS[Service.AUTH],
                    "env_file": ".env",
                    "log_level": "info",
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


if __name__ == "__main__":
    args = parse_arguments()
    if args.service is None:
        run_all()
    else:
        name = "main_microservices:" + args.service
        uvicorn.run(name, host="127.0.0.1", port=args.port, log_level="info")

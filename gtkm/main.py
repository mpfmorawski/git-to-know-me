from fastapi import FastAPI

from auth.service_auth import auth

app = FastAPI()

app.include_router(auth)
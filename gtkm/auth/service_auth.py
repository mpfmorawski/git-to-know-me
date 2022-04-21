from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import requests
import uuid

import crud, model, schemas
from database import engine, get_db

model.Base.metadata.create_all(bind=engine)
auth = APIRouter()

root_url = "http://127.0.0.1:8000"
client_id = "<CLIENT_ID>"
client_secret = "<CLIENT_SECRET>"
current_user_id = None


@auth.get("/auth/user/")
def get_user(id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if user:
        user_json = jsonable_encoder(user)
        return JSONResponse(content=user_json)
    else:
        return "No user with id: " + id + " exists in the database."


@auth.get("/api/auth/logout/")
def logout():
    global current_user_id
    current_user_id = None
    return 200


@auth.get("/auth/github/authorize")
def authorize_github():
    response = RedirectResponse(url=f"http://github.com/login/oauth/authorize?client_id={client_id}")
    return response


@auth.get("/auth/github/authorized", response_model=schemas.User)
def github_authorized(code : str, db: Session = Depends(get_db)):
    headers = {"Accept" : "application/vnd.github.v3+json"}
    params = {"client_id": client_id, "client_secret": client_secret, "code": code}
    token_request = requests.post("http://github.com/login/oauth/access_token", params=params, headers=headers)
    token = token_request.json()["access_token"]

    headers = {"Accept" : "application/vnd.github.v3+json", "Authorization" : "token " + token}
    login_request = requests.get("https://api.github.com/user?access_token=" + token, headers=headers)
    dict = login_request.json()
    login = dict["login"]

    try:
        user = crud.get_user(db, login)
        if not user:
            user_id = uuid.uuid4().hex
            user = schemas.User(id=user_id, github_login=login, github_token=token, gitlab_login="", gitlab_token="")
            crud.create_user(db=db, user=user)
        global current_user_id
        current_user_id = user.id
    except Exception as e:
        print(e)

    response = RedirectResponse(url=root_url + "/index.html")
    return response
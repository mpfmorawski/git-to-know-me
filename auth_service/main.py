from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import uvicorn
import urllib
import requests

import crud, model, schemas
from database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)
auth = FastAPI()

root_url = "http://127.0.0.1:8000"
redirect_page = "/authorized"
main_page = "/overview"
client_id = "<CLIENT_ID>"
client_secret = "<CLIENT_SECRET>"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@auth.get("/user")
def index(login: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, login)
    if user:
        user_json = jsonable_encoder(user)
        return JSONResponse(content=user_json)
    else:
        return get_authorization_response(login)

@auth.get("/authorize")
def index(login: str):
    return get_authorization_response(login)

@auth.get(redirect_page, response_model=schemas.User)
def index(login: str, code : str, db: Session = Depends(get_db)):
    headers = { "Accept" : "application/json" }
    params = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
    r = requests.post("http://github.com/login/oauth/access_token", params=params, headers=headers)
    dictionary = r.json()
    token = dictionary["access_token"]
    scope = dictionary["scope"]
    token_type = dictionary["token_type"]

    try:
        user = crud.get_user(db, login)
        if not user:
            user = schemas.User(login=login, token=token, scope=scope, token_type=token_type)
            crud.create_user(db=db, user=user)
    except Exception as e:
        print(e)

    response = RedirectResponse(url=root_url + "/overview")
    return response

def get_authorization_response(login):
    redirect_url = urllib.parse.quote(root_url + redirect_page + f"?login={login}")
    response = RedirectResponse(url=f'http://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_url}&login={login}')
    return response

if __name__ == "__main__":
    uvicorn.run(auth, host="127.0.0.1", port=8000)
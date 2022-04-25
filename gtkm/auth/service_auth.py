from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import requests
import uuid

from .database.database import Base, engine, get_db
from .database.user_schema import User
from .database.database_operations import get_user, get_user_by_github_login, create_user
from .sessions.session import backend, cookie, verifier
from .sessions.session_data import SessionData


Base.metadata.create_all(bind=engine)
auth = APIRouter()

CLIENT_ID = "<CLIENT_ID>"
CLIENT_SECRET = "<CLIENT_SECRET>"


# Endpoint for obtaining user data based on the user ID
@auth.get("/auth/user/")
async def get_user_data(id: str, db: Session = Depends(get_db)):
    user = get_user(db, id)
    if user:
        user_json = jsonable_encoder(user)
        return JSONResponse(content=user_json)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID does not exist.")


# Endpoint to end current user session
@auth.get("/api/auth/logout/")
async def logout(response: Response, session_id: uuid.UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    response.status_code = status.HTTP_200_OK
    return response


# Endpoint to redirect user after they clicked "Log in with GitHub"
@auth.get("/api/auth/github/authorize")
async def authorize_github():
    response = RedirectResponse(url=f"http://github.com/login/oauth/authorize?client_id={CLIENT_ID}")
    return response


# Endpoint that GitHub redirects the user to after successful authorization
@auth.get("/api/auth/github/authorized", response_model=User)
async def github_authorized(code : str, db: Session = Depends(get_db)):
    # Request exchanging the temporary code for the access token
    headers = {"Accept" : "application/json"}
    params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code}
    token_request = requests.post("http://github.com/login/oauth/access_token", params=params, headers=headers)
    token = token_request.json()["access_token"]
    # Request to check the logged in user's username
    headers = {"Accept" : "application/json", "Authorization" : "token " + token}
    login_request = requests.get("https://api.github.com/user?access_token=" + token, headers=headers)
    dict = login_request.json()
    login = dict["login"]
    # Get or create user in the DB
    user = get_user_by_github_login(db, login)
    if not user:
        user_id = uuid.uuid4().hex
        user = User(id=user_id, github_login=login, github_token=token, gitlab_login="", gitlab_token="")
        create_user(db=db, user=user)
    # Create user session and cookie
    response = RedirectResponse(url="/index.html")
    session = uuid.uuid4()
    data = SessionData(id=user.id)
    await backend.create(session, data)
    cookie.attach_to_response(response, session)
    return response
    

# Returns user ID based on current session cookie
@auth.get("/auth/user/id", dependencies=[Depends(cookie)])
async def get_user_id(session_data: SessionData = Depends(verifier)):
    return session_data
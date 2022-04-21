from fastapi import APIRouter

auth = APIRouter()


@auth.get("/auth/user/")
def get_user():
    return {"id": 111, "github": "zygfryd", "gitlab": None}


@auth.get("/api/auth/logout/")
def logout():
    return 200
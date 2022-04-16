from fastapi import FastAPI

app = FastAPI()


@app.get("/auth/user/")
def read_root():
    return {"id": 111, "github": "zygfryd"}


@app.get("/api/auth/logout/")
def read_root():
    return 200
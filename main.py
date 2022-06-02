from sample_credentials import sample_base
import uvicorn
import base64
from fastapi import FastAPI, Request


app = FastAPI(dependencies=[])


@app.get("/")
async def root(request: Request):
    return {"message": "Mock server is up and working. Send authorization requests to /auth/"}


@app.get("/auth/")
async def authorize_user(request: Request):
    if not request.headers.get("authorization"):
        return {"code": "ACCESS_DENIED", "message": "Access denied."}
    # get raw credentials
    credentials = request.headers["authorization"].split()[1]

    # decode
    decoded = base64.b64decode(credentials).decode("ascii")

    # check if credentials are valid or not
    username = decoded.split(sep=":")[0]
    password = decoded.split(sep=":")[1]

    if username not in sample_base:
        return {"code": "AUTHENTICATION_ERROR", "message": "Wrong login/password."}

    if username in sample_base and not password == sample_base[username].get("password"):
        return {"code": "AUTHENTICATION_ERROR", "message": "Wrong login/password."}

    if username in sample_base and password == sample_base[username].get("password"):
        return {
            "login": username,
            "isAdmin": sample_base[username].get("is_admin"),
            "spaceLimit": sample_base[username].get("space_limit"),
        }

    return {"message": "Something went wrong. Please contact administrator."}
    # decoded = base64.b64decode(credentials).decode("ascii")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8050)

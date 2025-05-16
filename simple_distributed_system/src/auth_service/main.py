import jwt
import uvicorn
import logging

from datetime import datetime, UTC, timedelta
from fastapi import FastAPI, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from pydantic import BaseModel


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def create_jwt_token(username: str, role: str) -> str:
    now = datetime.now(UTC)
    exp = datetime.now(UTC) + timedelta(days=1)

    encoded_jwt = jwt.encode(
        {
            "sub": username,
            "role": role,
            "iat": now.timestamp(),
            "exp": exp.timestamp(),
        },
        "secret",
        algorithm="HS256"
    )

    return encoded_jwt


logger = logging.getLogger(__name__)


app = FastAPI()


app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)


class AuthCredentials(BaseModel):
    login: str
    password: str


@app.post("/login")
def login(auth_credentials: AuthCredentials, response: Response):
    if auth_credentials.login == "admin" and auth_credentials.password == "admin":
        auth_token = create_jwt_token(auth_credentials.login, role="admin")
        return {"token": auth_token}

    if auth_credentials.login == "user" and auth_credentials.password == "user":
        auth_token = create_jwt_token(auth_credentials.login, role="user")
        return {"token": auth_token}

    response.status_code = 401


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=443,
        ssl_keyfile="ca.key",
        ssl_certfile="ca.crt",
    )

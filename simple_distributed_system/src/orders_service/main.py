import jwt
import logging
import uvicorn

from datetime import datetime, UTC

from fastapi import FastAPI, Header, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from typing import Annotated

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)


def parse_jwt_token(token: str) -> dict:
    decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
    logger.info(f"succesfully decoded jwt token: {decoded_token}")

    return decoded_token


ORDERS = [
    {
        "id": "1",
        "owner": "user",
        "name": "ice cream",
    },
    {
        "id": "2",
        "owner": "admin",
        "name": "milk",
    },
]


@app.get("/orders")
def orders(response: Response, test_hour: int = None, authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        logger.warning("Authorization token not provided")
        response.status_code = 401
        return

    try:
        parsed_token = parse_jwt_token(token=authorization)
    except Exception:
        logger.warning(f"Could not parse jwt token {authorization}")
        response.status_code = 401
        return

    now = datetime.now(UTC)
    hour = test_hour if test_hour is not None else now.hour
    if hour < 9 or hour > 18:
        logger.warning(f"Invalid access time token {authorization}")
        response.status_code = 403

        return {"error": "Outside business hours"}

    if parsed_token["role"] == "admin":
        return ORDERS

    return [x for x in ORDERS if x["owner"] == parsed_token["role"]]


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=443,
        ssl_keyfile="ca.key",
        ssl_certfile="ca.crt",
    )

from fastapi import Header, Request
from starlette_context import request_cycle_context
from .authentication import JWTAuthentication
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

async def authentication_middleware(
    Authentication = Header(default=None) ):
    # When used a Depends(), this function get the `X-Client_ID` header,
    # which will be documented as a required header by FastAPI.
    # use `authentication: str = Header(None)` for an optional header.    
    auth_instance = JWTAuthentication(Authentication, session = get_db())
    data = {"Authentication": auth_instance}
    with request_cycle_context(data):
        # yield allows it to pass along to the rest of the request
        yield

    


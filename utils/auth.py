from typing import List, Optional
import time
import uuid

from fastapi import Header, HTTPException

from utils.schemas import UserAuthTokenSchema

accessed_auth_tokens: List[UserAuthTokenSchema] = []


def create_new_token() -> UserAuthTokenSchema:
    """
    Generate and save new user token
    :return: User token and expiration timestamp
    """
    token = UserAuthTokenSchema(
        token=uuid.uuid4().hex,
        expire_at=int(time.time() * 1000) + (7 * 24 * 60 * 60 * 1000 + 10 * 1000)
        # 7 Days (not croissant) + 10 seconds
    )
    accessed_auth_tokens.append(token)
    return token


def check_token(token: str) -> bool:
    """
    Check is token valid and not expired
    :param token: User auth token
    :return: Is token valid
    """
    for auth_schema in accessed_auth_tokens:
        if auth_schema.token == token and auth_schema.expire_at > (time.time() * 1000):
            return True
    return False


async def verify_token_depend(authorization: Optional[str] = Header(None)):
    """
    User token verifying function. Every endpoint in User API depends on it
    """
    if not authorization:
        raise HTTPException(status_code=403)

    method, token = authorization.split(" ")
    if method.lower() == "bearer" and check_token(token):
        return token
    else:
        raise HTTPException(status_code=403)

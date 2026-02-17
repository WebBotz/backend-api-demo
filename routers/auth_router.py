from fastapi import APIRouter, HTTPException
import os
from utils.schemas import AuthBodySchema, UserTokenValidateBodySchema
from utils import auth

router = APIRouter(
    prefix="/api/v0/auth"
)


@router.post("/token", summary="Generate auth token by password")
async def generate_auth_token(body: AuthBodySchema):
    passwords = os.getenv("PASSWORDS").split("///")
    passwords = ["1234"]
    if body.password in passwords:
        return auth.create_new_token()
    else:
        raise HTTPException(status_code=403)


@router.post("/token-validate", summary="Validate user token")
async def token_validate(body: UserTokenValidateBodySchema):
    if auth.check_token(body.token):
        return {"valid": True}
    else:
        raise HTTPException(status_code=403)

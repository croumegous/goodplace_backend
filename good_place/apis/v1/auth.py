"""
API route for login
"""
# pylint: disable=missing-function-docstring
from fastapi import APIRouter, HTTPException

from good_place.apis.utils import verify_refresh_token
from good_place.core.security import create_jwt_token, verify_password
from good_place.crud.users import CRUDUser
from good_place.schemas.users import SchemaRefreshToken, SchemaUserLogin

router = APIRouter()


# POST /auth/login : allow user to login with email and password
@router.post("/login")
async def login(login_data: SchemaUserLogin):
    """
    Login with email and password
    """
    user = await CRUDUser.get_user_by_email(login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Bad username or password")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = create_jwt_token(subject=str(user.id))
    refresh_token = create_jwt_token(subject=str(user.id), refresh=True)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh_token")
async def refresh(payload: SchemaRefreshToken):
    """
    Refresh acces_token
    """
    user_id = await verify_refresh_token(payload.refresh_token)

    access_token = create_jwt_token(subject=user_id)
    return {"access_token": access_token}

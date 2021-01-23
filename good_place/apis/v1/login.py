"""
API route for login
"""
# pylint: disable=missing-function-docstring
from fastapi import APIRouter, HTTPException

from good_place.core.security import create_access_token, verify_password
from good_place.crud.users import CRUDUser
from good_place.schemas.users import SchemaUserLogin

router = APIRouter()


# POST /login : allow user to login with email and password
@router.post("/login")
async def login(login_data: SchemaUserLogin):
    user = await CRUDUser.get_user_by_email(login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Bad username or password")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token}

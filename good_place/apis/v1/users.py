"""
API route for users
"""
# pylint: disable=unused-argument
# pylint: disable=fixme
# pylint: disable=invalid-name
from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from good_place.apis.utils import get_current_user
from good_place.core.settings import CONFIG
from good_place.crud.users import CRUDUser
from good_place.db.models import Users
from good_place.schemas.users import SchemaUser, SchemaUserCreate

router = APIRouter()


# TODO change permission acces, implement current_user

# GET /users/ : get all users
@router.get("/", response_model=List[SchemaUser])
async def read_users(
    page: int = Query(1, ge=1, le=CONFIG.get("MAX_INT_32BITS")),
    perPage: int = Query(50, ge=1, le=CONFIG.get("MAX_INT_32BITS")),
) -> Any:
    """
    Get all users
    """
    return await CRUDUser.get_all_users(page=page, per_page=perPage)


# POST /users/ : create a new user
@router.post("/", response_model=SchemaUser)
async def create_user(user_data: SchemaUserCreate) -> Any:
    """
    Create new user
    """
    if await CRUDUser.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400, detail="A user with this email already exists"
        )
    if await CRUDUser.get_user_by_nickname(user_data.nickname):
        raise HTTPException(
            status_code=400, detail="A user with this nickname already exists"
        )
    if user_data.phone_number is not None and await CRUDUser.get_user_by_phone_number(
        user_data.phone_number
    ):
        raise HTTPException(
            status_code=400, detail="A user with this phone number already exists"
        )

    try:
        user = await CRUDUser.create_user(user_data)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while creating user in database: {exc}",
        ) from exc
    return user


@router.get("/{user_id}", response_model=SchemaUser)
async def read_user(user_id: UUID) -> Optional[SchemaUser]:
    """
    Get current user by its id.
    """
    return await CRUDUser.get_user(user_id)


# PUT /users/<user_id> : update user
@router.put("/{user_id}", response_model=SchemaUser)
async def update_user(user_id: UUID, user_data: SchemaUserCreate) -> Any:
    """
    Update own user
    """
    user = await CRUDUser.get_user(user_id)
    try:
        user = await CRUDUser.update_user(user, user_data)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while updating user in database: {exc}",
        ) from exc
    return user


# GET /users/me : get current_user profile
@router.get("/me", response_model=SchemaUser)
async def read_user_me(current_user: Users = Depends(get_current_user)) -> Any:
    """
    Get current user.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")
    return current_user


# PUT /users/me : update current_user profile
@router.put("/me", response_model=SchemaUser)
async def update_user_me(
    user_data: SchemaUserCreate, current_user: Users = Depends(get_current_user)
) -> Any:
    """
    Update own user
    """
    return None


# add current_user: Users = Depends(get_current_user)
# DELETE /users/{user_id} : delete a user by its id only available for admin
@router.delete("/{user_id}", response_model=SchemaUser)
async def delete_user_by_id(user_id: UUID) -> Any:
    """
    Delete specific user by its id
    """
    # if not(current_user.is_admin or current_user.id == user_id):
    #     raise HTTPException(status_code=400, detail="user doesn't have enough privileges")

    user = await CRUDUser.delete_user(user_id)
    return user

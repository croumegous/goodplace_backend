"""
API route for users
"""
# pylint: disable=unused-argument
# pylint: disable=fixme
# pylint: disable=invalid-name
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from good_place.apis.utils import get_current_admin, get_current_user
from good_place.core.settings import CONFIG
from good_place.crud.users import CRUDUser
from good_place.db.models import Users
from good_place.schemas.users import SchemaUser, SchemaUserCreate, SchemaUserList

router = APIRouter()


# GET /users/ : get all users
@router.get("/", response_model=SchemaUserList)
async def read_users(
    page: int = Query(1, ge=1, le=CONFIG.get("MAX_INT_32BITS")),
    perPage: int = Query(50, ge=1, le=CONFIG.get("MAX_INT_32BITS")),
    _: Users = Depends(get_current_admin),
) -> Any:
    """
    Get all users
    """
    all_users, count_users = await CRUDUser.get_all_users(page=page, per_page=perPage)

    return {"users": all_users, "count": count_users}


# POST /users/ : create a new user
@router.post("/", response_model=SchemaUser)
async def create_user(user_data: SchemaUserCreate) -> Any:
    """
    Create new user
    """
    await CRUDUser.check_no_duplicate_user(user_data)
    try:
        user = await CRUDUser.create_user(user_data)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while creating user in database: {exc}",
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
    user = await CRUDUser.get_user(current_user.id)
    await CRUDUser.check_no_duplicate_user(user_data, current_user.id)

    return await CRUDUser.update_user(user, user_data)


# DELETE /users/{user_id} : delete a user by its id only available for admin
@router.delete("/{user_id}", response_model=SchemaUser)
async def delete_user_by_id(
    user_id: UUID, current_user: Users = Depends(get_current_user)
) -> Any:
    """
    Delete specific user by its id
    """
    if not (current_user.is_admin or current_user.id == user_id):
        raise HTTPException(
            status_code=403, detail="Forbiden user doesn't have enough privileges"
        )

    return await CRUDUser.delete_user(user_id)

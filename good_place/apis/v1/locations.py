"""
API route for locations
"""
# pylint: disable=fixme
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from good_place.apis.utils import get_current_user
from good_place.crud.locations import CRUDLocation
from good_place.crud.users import CRUDUser
from good_place.db.models import Users
from good_place.schemas.locations import SchemaLocation, SchemaLocationCreate

router = APIRouter()


# TODO change permission acces, implement current_user

# GET /locations/<location_id> : get location by its id
@router.get("/{loc_id}", response_model=SchemaLocation)
async def read_location(loc_id: UUID) -> Any:
    """
    Get location by its id.
    """
    return await CRUDLocation.get_location(loc_id)


# GET /locations/me : get current_user location
@router.get("/me", response_model=SchemaLocation)
async def read_location_me(current_user: Users = Depends(get_current_user)) -> Any:
    """
    Get current user location.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")
    return CRUDLocation.get_location_by_user(current_user.id)


# POST /locations/ : create a new location
@router.post("/", response_model=SchemaLocation)
async def create_location(
    location_data: SchemaLocationCreate,
    current_user: Users = Depends(get_current_user),
) -> Any:
    """
    Create location for current user
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")
    if await CRUDLocation.location_by_user_exists(current_user.get("id")):
        raise HTTPException(
            status_code=400, detail="A location for this user already exists"
        )
    try:
        location = await CRUDLocation.create_location(location_data, current_user.id)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while creating location in database: {exc}",
        ) from exc
    return location


# PUT /locations/me : update current_user location
@router.put("/me", response_model=SchemaLocation)
async def update_location_me(
    location_data: SchemaLocationCreate,
    current_user: Users = Depends(get_current_user),
) -> Any:
    """
    Update current_user location
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")
    try:
        location = await CRUDLocation.update_location(
            location_data, current_user.get("id")
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while updating location in database: {exc}",
        ) from exc
    return location


# PUT /locations/me : update current_user location
@router.delete("/me", response_model=SchemaLocation)
async def delete_location_me(current_user: Users = Depends(get_current_user)) -> Any:
    """
    Delte current_user location
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")
    try:
        location = await CRUDLocation.delete_location(current_user.get("id"))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while deleting location in database: {exc}",
        ) from exc
    return location


############################################################################
#### ONLY for test purpose before implementaion of get_current user ########
############################################################################

# POST /locations/ : create a new location
@router.post("/{user_id}", response_model=SchemaLocation)
async def create_location_user_id(
    location_data: SchemaLocationCreate, user_id: UUID
) -> Any:
    """
    Create location for user_id
    """
    await CRUDUser.get_user(user_id)
    if await CRUDLocation.location_by_user_exists(user_id):
        raise HTTPException(
            status_code=400, detail="A location for this user already exists"
        )
    try:
        location = await CRUDLocation.create_location(location_data, user_id)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while creating location in database: {exc}",
        ) from exc
    return location


# PUT /locations/me : update current_user location
@router.put("/{user_id}", response_model=SchemaLocation)
async def update_location_user_id(
    location_data: SchemaLocationCreate, user_id: UUID
) -> Any:
    """
    Update user_id location
    """
    try:
        location = await CRUDLocation.update_location(location_data, user_id)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while updating location in database: {exc}",
        ) from exc
    return location


# PUT /locations/me : update current_user location
@router.delete("/{user_id}", response_model=SchemaLocation)
async def delete_location_user_id(user_id: UUID) -> Any:
    """
    Delete user_id location
    """
    try:
        location = await CRUDLocation.delete_location(user_id)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while deleting location in database: {exc}",
        ) from exc
    return location

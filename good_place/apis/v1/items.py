"""
API route for items
"""
# from typing import List
# pylint: disable=too-many-arguments
# pylint: disable=invalid-name

from typing import Any, List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from good_place.apis.utils import check_sort_field, get_current_user
from good_place.core.settings import CONFIG
from good_place.crud.categories import CRUDCategory
from good_place.crud.items import CRUDItem
from good_place.crud.locations import CRUDLocation
from good_place.crud.users import CRUDUser
from good_place.db.models import Users
from good_place.schemas.items import (
    SchemaFullItem,
    SchemaFullItemResponse,
    SchemaItem,
    SchemaItemCreate,
    SchemaItemResponse,
)

router = APIRouter()

# GET /items/: get list of items
@router.get("/", response_model=Union[SchemaFullItemResponse, SchemaItemResponse])
async def read_items(
    page: int = Query(1, ge=1, le=CONFIG.get("MAX_INT_32BITS")),
    perPage: int = Query(50, ge=1, le=CONFIG.get("MAX_INT_32BITS")),
    maxPrice: int = Query(None, ge=0, le=CONFIG.get("MAX_INT_32BITS")),
    category: str = None,
    search: str = "",
    sortField: str = None,
    details: bool = True,
) -> Any:
    """
    Returns a list of items with full informations.
    """
    if sortField:
        sortField = check_sort_field(SchemaItem, sortField)
    if category:
        category = await CRUDCategory.get_id_by_category_label(category)

    items, count, highest_price = await CRUDItem.get_all_items(
        max_price=maxPrice,
        sort_field=sortField,
        page=page,
        per_page=perPage,
        category=category,
        search=search,
        details=details,
    )

    return {"count": count, "items": items, "highestPrice": highest_price}


# GET /items/me : get curent user items
@router.get("/me", response_model=Union[List[SchemaFullItem], List[SchemaFullItem]])
async def read_my_items(current_user: Users = Depends(get_current_user)) -> Any:
    """
    Returns list of items of current user with full informations.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")

    return await CRUDItem.get_user_items(current_user.id)


# GET /items/<item_id> : get full information of item by its id
@router.get("/{item_id}", response_model=SchemaFullItem)
async def read_full_item(item_id: UUID) -> Any:
    """
    Returns full information about item by its id.
    """
    return await CRUDItem.get_item(item_id, details=True)


# POST /items/ : create a new item
# add current_user: Users = Depends(get_current_user)
@router.post("/", response_model=SchemaItem)
async def create_item(
    item_data: SchemaItemCreate,
    current_user: Users = Depends(get_current_user),
) -> Any:
    """
    Create item for current user
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")
    if not await CRUDLocation.location_by_user_exists(current_user.id):
        raise HTTPException(
            status_code=400, detail="User need to add a location to create items"
        )
    # try:
    #     item = await CRUDItem.create_item(item_data, current_user.id)
    # except Exception as exc:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"Error while creating item in database: {exc}",
    #     ) from exc
    return await CRUDItem.create_item(item_data, current_user.id)


# PUT /items/<item_id> : update current_user location
@router.put("/{item_id}", response_model=SchemaItem)
async def update_item(
    item_data: SchemaItemCreate,
    item_id: UUID,
    current_user: Users = Depends(get_current_user),
) -> Any:
    """
    Update item_id item
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")
    item = await CRUDItem.get_item(item_id, details=False)
    if current_user.id != item.user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbiden user is not the owner of the item specified",
        )

    item = await CRUDItem.update_item(item_data, item_id)
    return item


# PUT /items/<item_id> : update current_user location
@router.delete("/{item_id}", response_model=SchemaItem)
async def delete_item_by_id(
    item_id: UUID, current_user: Users = Depends(get_current_user)
) -> Any:
    """
    Update item_id item
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized need a logged user")
    item = await CRUDItem.get_item(item_id, details=False)
    if current_user.id != item.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Forbiden user doesn't have enough privileges"
        )

    item = await CRUDItem.delete_item(item_id)
    return item


############################################################################
#### ONLY for test purpose before implementaion of get_current user ########
############################################################################


# POST /items/<user_id> : create a new item
@router.post("/{user_id}", response_model=SchemaItem)
async def create_item_user_id(item_data: SchemaItemCreate, user_id: UUID) -> Any:
    """
    Create item for a user
    """
    await CRUDUser.get_user(user_id)
    if not await CRUDLocation.location_by_user_exists(user_id):
        raise HTTPException(
            status_code=400, detail="User need to add a location to create items"
        )
    try:
        item = await CRUDItem.create_item(item_data, user_id)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while creating item in database: {exc}",
        ) from exc
    return item

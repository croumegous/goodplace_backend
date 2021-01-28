"""
API route for categories
"""
# pylint: disable=missing-function-docstring
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from good_place.apis.utils import get_current_user
from good_place.crud.categories import CRUDCategory
from good_place.db.models import Users
from good_place.schemas.categories import SchemaCategory, SchemaCategoryCreate

router = APIRouter()


# GET /categories/ : get all available categories
@router.get("/", response_model=List[SchemaCategory])
async def get_categories():
    return await CRUDCategory.get_all_category()


# POST /categories/ : create a new category (admin only)
@router.post("/", response_model=SchemaCategory)
async def create_category(
    category: SchemaCategoryCreate, current_user: Users = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Forbiden user doesn't have enough privileges"
        )

    return await CRUDCategory.create_category(category)

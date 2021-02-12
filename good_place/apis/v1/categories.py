"""
API route for categories
"""
# pylint: disable=missing-function-docstring
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from good_place.apis.utils import get_current_admin
from good_place.crud.categories import CRUDCategory
from good_place.db.models import Users
from good_place.schemas.categories import SchemaCategory, SchemaCategoryCreate

router = APIRouter()


# GET /categories/ : get all available categories
@router.get("/", response_model=List[SchemaCategory])
async def get_categories():
    """
    Get all categories
    """
    return await CRUDCategory.get_all_category()


# POST /categories/ : create a new category (admin only)
@router.post("/", response_model=SchemaCategory, status_code=201)
async def create_category(
    category: SchemaCategoryCreate, _: Users = Depends(get_current_admin)
):
    """
    Create a new category (admin only)
    """
    return await CRUDCategory.create_category(category)


# PUT /categories/<category_id> : update a category by its id (admin only)
@router.put("/{category_id}", response_model=SchemaCategory)
async def update_category(
    category_id: UUID,
    category: SchemaCategoryCreate,
    _: Users = Depends(get_current_admin),
):
    """
    Update category by its id (admin only)
    """
    old_category = await CRUDCategory.get_category_by_id(category_id)
    return await CRUDCategory.update_category(old_category, category)


# DELETE /categories/<category_id> : delete a category by its id only available for admin
@router.delete("/{category_id}", status_code=204)
async def delete_category_by_id(
    category_id: UUID, _: Users = Depends(get_current_admin)
):
    """
    Delete category by its id (admin only)
    """
    return await CRUDCategory.delete_category(category_id)

"""
Categories CRUD
"""
import uuid
from typing import List

from fastapi import HTTPException
from tortoise.queryset import QuerySet

from good_place.db.models import Categories


class CRUDCategory:
    """
    All categories crud function
    """

    @staticmethod
    async def get_all_category() -> List[Categories]:
        """Return all categories in database"""
        return await QuerySet(Categories).all()

    @staticmethod
    async def create_category(category) -> Categories:
        """Create category in database

        Args:
            category (SchemaCategoryCreate): category to create
        Returns:
            Categories: the created category
        """
        return await Categories.create(id=uuid.uuid4(), label=category.label)

    @staticmethod
    async def get_category_by_id(category_id: uuid.UUID) -> Categories:
        """Return category by its category id

        Args:
            category_id (uuid.UUID): id of the category
        Raises:
            HTTPException: 404 if category not found
        Returns:
            Categories: category model
        """
        category = await QuerySet(Categories).filter(id=category_id).get_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    @staticmethod
    async def get_id_by_category(categories_name: str) -> uuid.UUID:
        """Get id of a category by its category name/label

        Args:
            categories_name (str): label of the category
        Raises:
            HTTPException: 404 if category not found
        Returns:
            uuid.UUID: id of the category
        """
        category_id = (
            await QuerySet(Categories).filter(label=categories_name).get_or_none()
        )
        if not category_id:
            raise HTTPException(status_code=404, detail="Category not found")
        return category_id.id

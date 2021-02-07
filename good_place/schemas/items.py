"""
Items schema
"""
# pylint: disable-all
from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, PositiveInt, validator

from good_place.schemas.categories import SchemaCategory
from good_place.schemas.conditions import SchemaCondition
from good_place.schemas.images import SchemaImageUrlOnly
from good_place.schemas.locations import SchemaLocation
from good_place.schemas.users import SchemaUser


class SchemaItem(BaseModel):
    """
    Schema for items to return
    """

    id: UUID
    user_id: UUID
    condition_id: Optional[UUID]
    category_id: UUID
    title: str
    description: str
    price: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SchemaItemCreate(BaseModel):
    """
    Schema for items creation
    """

    id: Optional[UUID]
    condition: Optional[str]
    category: str
    images: Optional[List[HttpUrl]]
    title: str
    description: str
    price: PositiveInt

    @validator("images")
    def validate_image_list_length(cls, value):
        if len(value) > 10:
            raise ValueError(
                f"Too many images you can have at most 10 images per items"
            )
        return value


class SchemaFullItem(BaseModel):
    """
    Schema for items to return
    """

    id: UUID
    condition: Optional[SchemaCondition]
    category: SchemaCategory
    user: SchemaUser
    location: SchemaLocation
    images_list: Optional[List[SchemaImageUrlOnly]]
    title: str
    description: str
    price: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SchemaFullItemResponse(BaseModel):
    items: List[SchemaFullItem]
    count: int
    highestPrice: int


class SchemaItemResponse(BaseModel):
    items: List[SchemaItem]
    count: int
    highestPrice: int

"""
Categories schema
"""
# pylint: disable-all
import re
from uuid import UUID

from pydantic import BaseModel, validator
from pydantic.networks import HttpUrl


class SchemaCategory(BaseModel):
    id: UUID
    label: str
    icon: str
    image: HttpUrl

    class Config:
        orm_mode = True


class SchemaCategoryCreate(BaseModel):
    label: str
    icon: str
    image: HttpUrl

    @validator("label", "icon")
    def validate_category(cls, value):
        if not re.match(r"[\w-]+", value):
            raise ValueError(f"{value} is not alphanumeric")
        return value

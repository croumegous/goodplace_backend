"""
Categories schema
"""
# pylint: disable-all
import re
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator


class SchemaCategory(BaseModel):
    id: UUID
    label: str

    class Config:
        orm_mode = True


class SchemaCategoryCreate(BaseModel):
    label: str

    @validator("label")
    def validate_category(cls, value):
        if not re.match(r"[\w-]+", value):
            raise ValueError(f"{value} is not alphanumeric")
        return value

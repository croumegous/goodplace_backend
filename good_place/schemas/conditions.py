"""
Conditions schema
"""
# pylint: disable-all
import re
from uuid import UUID

from pydantic import BaseModel, validator


class SchemaCondition(BaseModel):
    id: UUID
    label: str

    class Config:
        orm_mode = True


class SchemaConditionCreate(BaseModel):
    label: str

    @validator("label")
    def validate_condition(cls, value):
        if not re.match(r"[\w-]+", value):
            raise ValueError(f"{value} is not alphanumeric")
        return value

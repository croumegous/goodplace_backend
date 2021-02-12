"""
Locations schema
"""

import re

# pylint: disable-all
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, validator


class SchemaLocation(BaseModel):
    """
    Basic schema for locations to be returned
    """

    id: UUID
    user_id: UUID
    country: str
    state: Optional[str]
    city: str
    street: str
    street_number: Optional[str]
    address_complement: Optional[str]
    postal_code: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SchemaLocationCreate(BaseModel):
    """
    Schema for user creation
    """

    country: constr(min_length=2)
    state: Optional[str]
    city: constr(min_length=2)
    street: constr(min_length=2)
    street_number: Optional[str]
    address_complement: Optional[str]
    postal_code: constr(min_length=2)

    class Config:
        orm_mode = True

    @validator(
        "country",
        "state",
        "city",
        "street",
        "street_number",
        "address_complement",
        "postal_code",
    )
    def validate_location(cls, value):
        if not re.match(r"[\w-]*", value):
            raise ValueError(f"{value} is not alphanumeric")
        return value

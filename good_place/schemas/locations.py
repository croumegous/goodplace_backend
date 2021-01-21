"""
Locations schema
"""

# pylint: disable-all
import re
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ValidationError, constr, validator


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

    class Config:
        orm_mode = True


class SchemaLocationCreate(BaseModel):
    """
    Schema for user creation
    """

    id: Optional[UUID]
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
        if not re.match(r"[\w-]+", value):
            raise ValidationError(f"{value} is not alphanumeric")
        return value

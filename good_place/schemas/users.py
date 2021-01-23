"""
Users schema
"""

# pylint: disable-all
import re
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ValidationError, constr, validator


class SchemaUser(BaseModel):
    """
    Basic schema for user to be returned
    """

    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str]
    nickname: str
    is_admin: bool
    avatar_url: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class SchemaUserCreate(BaseModel):
    """
    Schema for user creation
    """

    id: Optional[UUID]
    first_name: constr(min_length=2)
    last_name: constr(min_length=2)
    email: EmailStr
    phone_number: Optional[str]
    nickname: constr(min_length=2)
    password: constr(min_length=8)
    is_admin: Optional[bool]

    @validator("first_name", "last_name", "phone_number", "nickname")
    def validate_user(cls, value):
        if not re.match(r"[\w-]+", value):
            raise ValidationError(f"{value} is not alphanumeric")
        return value

    @validator("password")
    def validate_password(cls, value):
        if not re.match(r"[\w@_!#$%^&*=()<>?/|}{~:\]\\\[]+", value):
            raise ValidationError(f"{value} contains unsupported character")
        return value

    class Config:
        orm_mode = True


class SchemaUserLogin(BaseModel):
    """
    Basic schema for login authentication
    """

    email: EmailStr
    password: constr(min_length=8)

    @validator("password")
    def validate_password(cls, value):
        if not re.match(r"[\w@_!#$%^&*=()<>?/|}{~:\]\\\[]+", value):
            raise ValidationError(f"{value} contains unsupported character")
        return value

    class Config:
        orm_mode = True

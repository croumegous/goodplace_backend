"""
Users schema
"""

# pylint: disable-all
import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, HttpUrl, constr, validator


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
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SchemaUserList(BaseModel):
    """
    Basic schema for list of user
    """

    users: List[SchemaUser]
    count: int


class SchemaUserCreate(BaseModel):
    """
    Schema for user creation
    """

    first_name: constr(min_length=2)
    last_name: constr(min_length=2)
    email: EmailStr
    phone_number: Optional[str]
    avatar_url: Optional[str]
    nickname: constr(min_length=2)
    password: constr(min_length=8)

    @validator("first_name", "last_name", "phone_number", "nickname")
    def validate_user(cls, value):
        if not re.match(r"[\w-]*", value):
            raise ValueError(f"{value} is not alphanumeric")
        return value

    @validator("password")
    def validate_password(cls, value):
        if not re.match(r"[\w@_!#$%^&*=()<>?/|}{~:\]\\\[]+", value):
            raise ValueError(f"{value} contains unsupported character")
        return value

    class Config:
        orm_mode = True


class SchemaUserLogin(BaseModel):
    """
    Schema for login authentication
    """

    email: EmailStr
    password: constr(min_length=8)

    @validator("password")
    def validate_password(cls, value):
        if not re.match(r"[\w@_!#$%^&*=()<>?\/|}{~:\]\\[\"\'À-ú,._0-9 ()\-\+;]", value):
            raise ValueError(f"{value} contains unsupported character")
        return value


class SchemaRefreshToken(BaseModel):
    """
    Schema used to refresh JWT token
    """

    refresh_token: str

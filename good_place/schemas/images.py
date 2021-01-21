"""
Conditions schema
"""
# pylint: disable-all
import re
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, ValidationError, validator


class SchemaImage(BaseModel):
    id: UUID
    image_url: HttpUrl
    item: UUID

    class Config:
        orm_mode = True


class SchemaImageUrlOnly(BaseModel):
    image_url: HttpUrl

    class Config:
        orm_mode = True

"""
This is where we define users model
"""
#  pylint: disable=too-few-public-methods
#  pylint: disable=missing-class-docstring

import uuid

from tortoise import fields
from tortoise.models import Model


class Users(Model):
    """
    User represent a user account, it is necessary to create items
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    first_name = fields.CharField(max_length=50, null=False)
    last_name = fields.CharField(max_length=50, null=False)
    email = fields.CharField(max_length=255, null=False, unique=True)
    phone_number = fields.CharField(max_length=20, null=True, unique=True)
    nickname = fields.CharField(max_length=50, null=False, unique=True)
    password = fields.CharField(max_length=60, null=False)
    is_admin = fields.BooleanField(null=False, default=False)
    avatar_url = fields.CharField(max_length=500, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def full_name(self) -> str:
        """
        Returns the user's full_name
        """
        return f"{self.first_name} {self.last_name}".strip()

    # async def to_dict(self):
    #     """
    #     Parse a Tortoise model into a dict

    #     Returns:
    #         Dict: Model information
    #     """
    #     user = {}
    #     for field in self._meta.db_fields:
    #         user[field] = getattr(self, field)
    #     for field in self._meta.backward_fk_fields:
    #         user[field] = await getattr(self, field).all().values()
    #     return user

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password"]

"""
This is where we define items model
"""
#  pylint: disable=too-few-public-methods

import uuid

from tortoise import fields
from tortoise.models import Model


class Items(Model):
    """
    Represent an ad, someting to be sold by the user who create this ad
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    user = fields.ForeignKeyField("models.Users", related_name="items", null=False)
    condition = fields.ForeignKeyField(
        "models.Conditions", related_name="items", null=True
    )
    category = fields.ForeignKeyField(
        "models.Categories", related_name="items", null=False
    )
    title = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=5000, null=False)
    price = fields.IntField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

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

"""
This is where we define categories model
"""
#  pylint: disable=too-few-public-methods

import uuid

from tortoise import fields
from tortoise.models import Model


class Categories(Model):
    """
    Represent the category of the ad, for example "car", "toys", "gardening" ...
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    label = fields.CharField(max_length=50, null=False, unique=True)
    icon = fields.CharField(max_length=50, null=True)
    image = fields.CharField(max_length=500, null=True)

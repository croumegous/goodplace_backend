"""
This is where we define images model
"""
#  pylint: disable=too-few-public-methods

import uuid

from tortoise import fields
from tortoise.models import Model


class Images(Model):
    """
    Image represent the url image used to highlight an item
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    image_url = fields.CharField(max_length=500, null=False)
    item = fields.ForeignKeyField("models.Items", related_name="images", null=False)

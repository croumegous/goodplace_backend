"""
This is where we define status model
"""
#  pylint: disable=too-few-public-methods

import uuid

from tortoise import fields
from tortoise.models import Model


class Conditions(Model):
    """
    Represent the condition of the object/content of the ad, this field is not mandatory
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    label = fields.CharField(max_length=50, null=False)

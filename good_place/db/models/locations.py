"""
This is where we define locations model
"""
#  pylint: disable=too-few-public-methods
import uuid

from tortoise import fields
from tortoise.models import Model


class Locations(Model):
    """
    Location represent a the location of an user useful to find near items
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    user = fields.ForeignKeyField(
        "models.Users",
        related_name="location",
        on_delete=fields.CASCADE,
        unique=True,
        null=False,
    )
    country = fields.CharField(max_length=50, null=False)
    state = fields.CharField(max_length=50, null=True)
    city = fields.CharField(max_length=50, null=False)
    street = fields.CharField(max_length=100, null=False)
    street_number = fields.CharField(max_length=20, null=True)
    address_complement = fields.CharField(max_length=100, null=True)
    postal_code = fields.CharField(max_length=20, null=False)
    updated_at = fields.DatetimeField(auto_now=True)

"""
Custom field to use TsVector in DB
"""
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
from typing import Any

from tortoise import fields


class TsVectorField(fields.Field, str):
    """
    Custom field to use TsVector in DB
    """

    SQL_TYPE = None

    class _db_postgres:
        SQL_TYPE = "TSVECTOR"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def to_python_value(self, value: Any) -> Any:
        """
        Converts from the DB type to the Python type.

        :param value: Value from DB
        """
        return str(value)

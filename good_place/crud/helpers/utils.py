"""
Utils for CRUD functions
"""
# pylint: disable=missing-class-docstring
import enum

from pypika import CustomFunction


class Comp(enum.Enum):
    match = "@@"


to_tsquery = CustomFunction("to_tsquery", ["text"])

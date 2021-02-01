"""
This override of CountQuery is used to make full text search work with Tortoise ORM
"""
# pylint: disable-all
from typing import Any, Dict, List, Optional, Type, TypeVar

from pypika import Criterion
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.functions import Count
from tortoise.query_utils import Q
from tortoise.queryset import CountQuery

MODEL = TypeVar("MODEL", bound="Model")


class CriterionCountQuery(CountQuery):
    __slots__ = (
        "q_objects",
        "annotations",
        "custom_filters",
        "limit",
        "offset",
        "criterions",
    )

    def __init__(
        self,
        model: Type[MODEL],
        db: BaseDBAsyncClient,
        q_objects: List[Q],
        annotations: Dict[str, Any],
        custom_filters: Dict[str, Dict[str, Any]],
        limit: Optional[int],
        criterions: Optional[Criterion],
        offset: Optional[int],
    ) -> None:
        super().__init__(
            model, db, q_objects, annotations, custom_filters, limit, offset
        )
        self.criterions = criterions

    def _make_query(self) -> None:
        super()._make_query()
        for criterion in self.criterions:
            self.query._wheres &= criterion

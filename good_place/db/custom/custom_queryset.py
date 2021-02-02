"""
This override of QuerySet is used to make full text search work with Tortoise ORM
"""
# pylint: disable-all
import typing as tp
from copy import copy

from pypika.terms import BasicCriterion
from tortoise import Model
from tortoise.queryset import QuerySet

from good_place.db.custom.custom_countquery import CriterionCountQuery


class CriterionQuerySet(QuerySet):
    __slots__ = QuerySet.__slots__ + ("_criterions",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._criterions: tp.List[BasicCriterion] = []

    @classmethod
    def from_model(cls, model: tp.Type[Model]) -> "CriterionQuerySet":
        """"""
        return cls(model)

    def set_criterion(self, criterion: BasicCriterion) -> None:
        self._criterions.append(criterion)
        # self._criterions = criterion

    def _clone(self):
        """We need to copy all method because Tortoise use Specific class"""
        # here can be queryset = self.__class__.__new__(self.__class__)
        queryset = CriterionQuerySet.__new__(CriterionQuerySet)
        queryset.fields = self.fields
        queryset.model = self.model
        queryset.query = self.query
        queryset.capabilities = self.capabilities
        queryset._prefetch_map = copy(self._prefetch_map)
        queryset._prefetch_queries = copy(self._prefetch_queries)
        queryset._single = self._single
        queryset._raise_does_not_exist = self._raise_does_not_exist
        queryset._db = self._db
        queryset._limit = self._limit
        queryset._offset = self._offset
        queryset._fields_for_select = self._fields_for_select
        queryset._filter_kwargs = copy(self._filter_kwargs)
        queryset._orderings = copy(self._orderings)
        queryset._joined_tables = copy(self._joined_tables)
        queryset._q_objects = copy(self._q_objects)
        queryset._distinct = self._distinct
        queryset._annotations = copy(self._annotations)
        queryset._having = copy(self._having)
        queryset._custom_filters = copy(self._custom_filters)
        queryset._group_bys = copy(self._group_bys)
        queryset._select_for_update = self._select_for_update
        queryset._select_related = self._select_related
        queryset._select_related_idx = self._select_related_idx
        queryset._criterions = self._criterions
        return queryset

    def count(self) -> "CountQuery":
        """
        Return count of objects in queryset instead of objects.
        """
        return CriterionCountQuery(
            db=self._db,
            model=self.model,
            q_objects=self._q_objects,
            annotations=self._annotations,
            custom_filters=self._custom_filters,
            limit=self._limit,
            criterions=self._criterions,
            offset=self._offset,
        )

    def _make_query(self) -> None:
        super()._make_query()
        for criterion in self._criterions:
            self.query._wheres &= criterion

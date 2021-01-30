"""
Conditions CRUD
"""
import uuid

from fastapi import HTTPException
from tortoise.queryset import QuerySet

from good_place.db.models import Conditions


class CRUDCondition:
    """
    All conditions crud function
    """

    @staticmethod
    async def get_condition_by_id(condition_id: uuid.UUID) -> Conditions:
        """Return condition by its id

        Args:
            condition_id (uuid.UUID): id of the condition
        Raises:
            HTTPException: 404 if condition not found in database
        Returns:
            Conditions: condition model
        """
        condition = await QuerySet(Conditions).filter(id=condition_id).get_or_none()
        if not condition:
            raise HTTPException(status_code=404, detail="Condition not found")
        return condition

    @staticmethod
    async def get_id_by_condition_label(condition_name: str) -> uuid.UUID:
        """Return id of a condition by its name/label

        Args:
            condition_name (str): label of the condition

        Raises:
            HTTPException: 404 if condition not found

        Returns:
            uuid.UUID: id of the condition
        """
        condition_id = (
            await QuerySet(Conditions).filter(label=condition_name).get_or_none()
        )
        if not condition_id:
            raise HTTPException(status_code=404, detail="Condition not found")
        return condition_id.id

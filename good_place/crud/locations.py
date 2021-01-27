"""
Locations CRUD
"""
import uuid

from fastapi import HTTPException
from tortoise.queryset import QuerySet

from good_place.db.models import Locations
from good_place.schemas.locations import SchemaLocationCreate


class CRUDLocation:
    """
    All users's crud function
    """

    @staticmethod
    async def get_location(location_id: uuid.UUID) -> Locations:
        """Get location model by its id

        Args:
            location_id (uuid.UUID): id of the location
        Raises:
            HTTPException: 404 if location not found in database
        Returns:
            Locations: location model
        """

        location = await QuerySet(Locations).filter(id=location_id).get_or_none()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location

    @staticmethod
    async def location_by_user_exists(user_id: uuid.UUID) -> bool:
        """Check if a location exist for a specified user

        Args:
            user_id (uuid.UUID): id of the user to check location existance
        Returns:
            Boolean: True if location exists, false otherwise
        """
        return await Locations.exists(user_id=user_id)

    @staticmethod
    async def get_location_by_user(
        user_id: uuid.UUID, allow_fail: bool = False
    ) -> Locations:
        """Return location of the user

        Args:
            user_id (uuid.UUID): user to get location of
        Raises:
            HTTPException: 404 if no location found in database
        Returns:
            Locations: location model related to user
        """
        location = await QuerySet(Locations).filter(user_id=user_id).get_or_none()
        if not location and not allow_fail:
            raise HTTPException(
                status_code=404, detail=f"Location related to user {user_id} not found"
            )
        return location

    @staticmethod
    async def create_location(
        location: SchemaLocationCreate, user_id: uuid.UUID
    ) -> Locations:
        """Create a location for user in database

        Args:
            location (SchemaLocationCreate): Schema which contains all location data
            user_id (uuid.UUID): user id to whom assign location
        Returns:
            Locations: newly created location model
        """
        location.id = uuid.uuid4() if not location.id else location.id
        db_location = await Locations.create(
            id=location.id,
            user_id=user_id,
            country=location.country,
            state=location.state,
            city=location.city,
            street=location.street,
            street_number=location.street_number,
            address_complement=location.address_complement,
            postal_code=location.postal_code,
        )
        return db_location

    @staticmethod
    async def update_location(
        update_data: SchemaLocationCreate, user_id: uuid.UUID
    ) -> Locations:
        """Update location in database

        Args:
            update_data (SchemaLocationCreate): Schema which contains new location data
            user_id (uuid.UUID): user id to whom assign location
        Returns:
            Locations: updated location model
        """
        update_data = update_data.dict(exclude_unset=True)
        location = await CRUDLocation.get_location_by_user(user_id)
        location.update_from_dict(update_data)
        await location.save(force_update=False)
        return location

    @staticmethod
    async def delete_location(user_id: uuid.UUID) -> Locations:
        """Delete location in database

        Args:
            user_id (uuid.UUID): user id to whom delete the location
        Returns:
            Locations: deleted location model
        """
        location = await CRUDLocation.get_location_by_user(user_id)
        await location.delete()

        return location

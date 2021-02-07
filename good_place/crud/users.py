# pylint: disable=no-self-use
"""
Users CRUD
"""
import uuid
from typing import List, Optional

from fastapi import HTTPException
from tortoise.queryset import Q, QuerySet

from good_place.core.security import get_password_hashed
from good_place.db.models import Users
from good_place.schemas.users import SchemaUserCreate


class CRUDUser:
    """
    All users's crud function
    """

    @staticmethod
    async def get_all_users(page: int = 1, per_page: int = 50) -> List[Users]:
        """Get list of user with pagination

        Args:
            page (int, optional): number of the page to get. Defaults to 1.
            per_page (int, optional): number of users to show in one page. Defaults to 50.
        Returns:
            List[Users]: Users models
        """
        count_users = await QuerySet(Users).count()
        all_users = (
            await QuerySet(Users).offset((page - 1) * per_page).limit(per_page).all()
        )

        return all_users, count_users

    @staticmethod
    async def get_user(user_id: uuid.UUID) -> Users:
        """get one user by its id

        Args:
            user_id (uuid.UUID): user id to fetch in database
        Raises:
            HTTPException: 404 if user not found
        Returns:
            Users: user model
        """
        user = await QuerySet(Users).filter(id=user_id).get_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def get_user_by_email(
        email: str, except_id: Optional[uuid.UUID] = None
    ) -> Users:
        """get one user by its email

        Args:
            email (str): email of the user to fetch
            except_id (UUID): avoid this user id, useful when searching for duplicate on update user
        Returns:
            Users: user model or None if not found
        """
        if not except_id:
            return await QuerySet(Users).filter(email=email).get_or_none()
        return (
            await QuerySet(Users)
            .filter(Q(email=email) & ~Q(id=except_id))
            .get_or_none()
        )

    @staticmethod
    async def get_user_by_nickname(
        nickname: str, except_id: Optional[uuid.UUID] = None
    ) -> Users:
        """get one user by its nickname

        Args:
            nickname (str): nickname of the user to fetch
            except_id (UUID): avoid this user id, useful when searching for duplicate on update user
        Returns:
            Users: User model or None if not found
        """
        if not except_id:
            return await QuerySet(Users).filter(nickname=nickname).get_or_none()
        return (
            await QuerySet(Users)
            .filter(Q(nickname=nickname) & ~Q(id=except_id))
            .get_or_none()
        )

    @staticmethod
    async def get_user_by_phone_number(
        phone_number: str, except_id: Optional[uuid.UUID] = None
    ) -> Users:
        """get one user by its phone number

        Args:
            phone_number (str): phone number of the user to fetch
            except_id (UUID): avoid this user id, useful when searching for duplicate on update user
        Returns:
            Users: User model or None if not found
        """
        if not except_id:
            return await QuerySet(Users).filter(phone_number=phone_number).first()
        return (
            await QuerySet(Users)
            .filter(Q(phone_number=phone_number) & ~Q(id=except_id))
            .get_or_none()
        )

    @staticmethod
    async def create_user(user: SchemaUserCreate) -> Users:
        """Create a new user in database

        Args:
            user (SchemaUserCreate): Schema which contains all location data
        Returns:
            Users: user model newly created
        """
        user.id = uuid.uuid4() if not user.id else user.id
        db_user = await Users.create(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            avatar_url=user.avatar_url,
            nickname=user.nickname,
            password=get_password_hashed(user.password),
            is_admin=False,
        )
        return db_user

    @staticmethod
    async def update_user(user: Users, update_data: SchemaUserCreate) -> Users:
        """Update user in database

        Args:
            user (Users): user model to update
            update_data (SchemaUserCreate): Schema which contains new user data

        Returns:
            Users: updated user model
        """

        if update_data.password:
            update_data.password = get_password_hashed(update_data.password)
        update_data = update_data.dict(exclude_unset=True)
        user.update_from_dict(update_data)
        await user.save(force_update=False)
        return user

    @staticmethod
    async def delete_user(user_id: uuid.UUID) -> Users:
        """Delete a user in database by its id

        Args:
            user_id (uuid.UUID): user id of the user to delete
        Returns:
            Users: deleted user model
        """
        user = await CRUDUser.get_user(user_id)
        await user.delete()

        return user

    @staticmethod
    async def check_no_duplicate_user(
        user_data: Users, update_id: Optional[uuid.UUID] = None
    ):
        """Check value of user to upsert in database don't violate UNIQUE value constraint

        Args:
            user_data (Users): data of user to upsert in database
            update_id (UUID): useful on update not to find duplicate value with current user
                                if this value hasn't been changed. Defaults to None.

        Raises:
            HTTPException 400: if value is a duplicate of unique value in database
        """
        if await CRUDUser.get_user_by_email(user_data.email, except_id=update_id):
            raise HTTPException(
                status_code=400, detail="A user with this email already exists"
            )
        if await CRUDUser.get_user_by_nickname(user_data.nickname, except_id=update_id):
            raise HTTPException(
                status_code=400, detail="A user with this nickname already exists"
            )
        if (
            user_data.phone_number is not None
            and await CRUDUser.get_user_by_phone_number(
                user_data.phone_number, except_id=update_id
            )
        ):
            raise HTTPException(
                status_code=400, detail="A user with this phone number already exists"
            )

"""
items CRUD
"""
# pylint: disable=too-many-arguments
# pylint: disable=line-too-long

import uuid
from typing import List

from fastapi import HTTPException
from pypika import Table
from pypika.terms import BasicCriterion
from tortoise.queryset import QuerySet

from good_place.crud.categories import CRUDCategory
from good_place.crud.conditions import CRUDCondition
from good_place.crud.helpers.utils import Comp, to_tsquery
from good_place.crud.images import CRUDImage
from good_place.db.custom.custom_queryset import CriterionQuerySet
from good_place.db.models import Items
from good_place.schemas.items import SchemaItemCreate


class CRUDItem:
    """
    All items crud function
    """

    @staticmethod
    async def get_item(item_id: uuid.UUID, details: bool = True) -> Items:
        """get item information by its id

        Args:
            item_id (uuid.UUID): id of the item to fecth
            details (bool): if True fetch details of item
        Raises:
            HTTPException: 404 if item not found
        Returns:
            Items: item model
        """
        item_query = QuerySet(Items).filter(id=item_id)

        if not details:
            item = await item_query.get_or_none()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item

        item = await item_query.prefetch_related(
            "category", "condition", "user", "images", "user__location"
        ).get_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if item.user.location.related_objects:
            item.location = item.user.location.related_objects[0]
        item.images_list = item.images.related_objects
        return item

    @staticmethod
    async def get_all_items(
        max_price: int,
        sort_field: str,
        page: int = 1,
        per_page: int = 50,
        category: uuid.UUID = None,
        search: str = None,
    ) -> List[Items]:
        """get list of item with pagination

        Args:
            max_price (int): filter result with price can be None
            sort_field (str): field use to sort by can be None. e.g : +price (ascending price)
                                                            -created_at (descending created_at)
            page (int, optional): number of the page to get. Defaults to 1.
            per_page (int, optional): number of items to show in one page. Defaults to 50.
        Returns:
            all_items (List[Items]): list of item model
            count_results (int): number of items
            highest_price.price (int): higgest price of items (all items not only paginated)
        """

        items_query = QuerySet(Items)

        # I'm obliged to override tortoise functions with pypika to use full text search as it's not implemented yet
        if search != "":
            items = Table("items")
            items_query = CriterionQuerySet(Items)
            items_query.set_criterion(
                BasicCriterion(
                    Comp.match,
                    items.text_search_vector,
                    to_tsquery(search.replace(" ", " | ")),
                )
            )
        if category:
            items_query = items_query.filter(category_id=category)

        # not ideal
        highest_price = await items_query.only("price").order_by("-price").first()

        if max_price is not None:
            items_query = items_query.filter(price__lte=max_price)
        if sort_field:
            items_query = items_query.order_by(sort_field)

        count_results = await items_query.count()

        items_query = items_query.offset((page - 1) * per_page).limit(per_page)

        all_items = await items_query.prefetch_related(
            "category", "condition", "user", "images", "user__location"
        )
        for item in all_items:
            if item.user.location.related_objects:
                item.location = item.user.location.related_objects[0]
            item.images_list = item.images.related_objects

        if not highest_price:
            return all_items, count_results, 0
        return all_items, count_results, highest_price.price

    @staticmethod
    async def get_user_items(user_id) -> List[Items]:
        """get list of item with pagination

        Args:
            max_price (int): filter result with price can be None
            sort_field (str): field use to sort by can be None. e.g : +price (ascending price)
                                                            -created_at (descending created_at)
            page (int, optional): number of the page to get. Defaults to 1.
            per_page (int, optional): number of items to show in one page. Defaults to 50.
            details (bool, opt): if True get details of items like user informations. Default True
        Returns:
            List[Items]: list of item model
        """

        all_items = (
            await QuerySet(Items)
            .filter(user_id=user_id)
            .prefetch_related(
                "category", "condition", "user", "images", "user__location"
            )
        )
        for item in all_items:
            if item.user.location.related_objects:
                item.location = item.user.location.related_objects[0]
            item.images_list = item.images.related_objects
        return all_items

    @staticmethod
    async def create_item(item: SchemaItemCreate, user_id: uuid.UUID) -> Items:
        """Create a new item in database

        Args:
            item (SchemaItemCreate): Schema which contains item data
            user_id (uuid.UUID): user that will be linked to the item
        Returns:
            Items: Newly created item model
        """
        condition_id = None
        if item.condition:
            condition_id = await CRUDCondition.get_id_by_condition_label(item.condition)
        category_id = await CRUDCategory.get_id_by_category_label(item.category)
        item_id = uuid.uuid4()
        db_item = await Items.create(
            id=item_id,
            user_id=user_id,
            condition_id=condition_id,
            category_id=category_id,
            title=item.title,
            description=item.description,
            price=item.price,
        )
        if item.images:
            await CRUDImage.create_image_for_item(item.images, item_id)

        return db_item

    @staticmethod
    async def update_item(update_data: SchemaItemCreate, item_id: uuid.UUID) -> Items:
        """Update item in database

        Args:
            update_data (SchemaItemCreate): Schema which contains new item data
            item_id (uuid.UUID): item to update
        Returns:
            Items: Updated item model
        """
        update_data = update_data.dict(exclude_unset=True)
        new_images = update_data.pop("images", [])

        update_data["condition_id"] = await CRUDCondition.get_id_by_condition_label(
            update_data.get("condition")
        )
        update_data["category_id"] = await CRUDCategory.get_id_by_category_label(
            update_data.get("category")
        )
        await CRUDImage.update_images_of_item(new_images, item_id)
        item = await CRUDItem.get_item(item_id, details=False)

        update_data.pop("condition", None)
        update_data.pop("category", None)
        item.update_from_dict(update_data)
        await item.save(force_update=True)
        return item

    @staticmethod
    async def delete_item(item_id: uuid.UUID):
        """Delete an item in database by its id

        Args:
            item_id (uuid.UUID): item id to delete
        """
        item = await CRUDItem.get_item(item_id, details=False)
        return await item.delete()

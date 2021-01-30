# pylint: disable=no-name-in-module
"""
Images CRUD
"""
import uuid
from typing import List

from pydantic.networks import HttpUrl
from tortoise.queryset import QuerySet

from good_place.db.models import Images


class CRUDImage:
    """
    All images crud function
    """

    @staticmethod
    async def create_image_for_item(images: List[HttpUrl], item_id: uuid.UUID):
        """Create images in database

        Args:
            images (List[HttpUrl]): [description]
            item_id (uuid.UUID): [description]
        """

        for image in set(str(img) for img in images if img.strip() != ""):
            await Images.create(
                id=uuid.uuid4(),
                image_url=image,
                item_id=item_id,
            )

    @staticmethod
    async def update_images_of_item(images: List[HttpUrl], item_id: uuid.UUID):
        """Update images of item in database

        Args:
            images (List[HttpUrl]): List of new images
            item_id (uuid.UUID): item id of the item related to those images
        """
        new_images = set(map(str, images))
        current_images = await QuerySet(Images).filter(item_id=item_id).all()

        current_img_url = set(image.image_url for image in current_images)
        to_add = [image for image in new_images if image not in current_img_url]
        to_delete = [image for image in current_img_url if image not in new_images]

        for image in to_add:
            await Images.create(
                id=uuid.uuid4(),
                image_url=image,
                item_id=item_id,
            )

        for image in current_images:
            if image.image_url in to_delete:
                await image.delete()

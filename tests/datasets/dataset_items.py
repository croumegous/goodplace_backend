# pylint: skip-file

"""
Dataset for items tests
"""

import datetime
import uuid

from good_place.db.models import Categories, Conditions, Items, Users

CATEGORY_CAR_ID = str(uuid.uuid4())
CATEGORY_HOUSE_ID = str(uuid.uuid4())
CATEGORY_JEWELRY_ID = str(uuid.uuid4())
CATEGORY_TOOLS_ID = str(uuid.uuid4())
CATEGORY_GAMING_ID = str(uuid.uuid4())
CATEGORY_COMPUTER_ID = str(uuid.uuid4())
CATEGORY_BIKES_ID = str(uuid.uuid4())


CONDITION_NEW_ID = str(uuid.uuid4())
CONDITION_LIKENEW_ID = str(uuid.uuid4())
CONDITION_EXCELLENT_ID = str(uuid.uuid4())
CONDITION_GOOD_ID = str(uuid.uuid4())
CONDITION_USED_ID = str(uuid.uuid4())
CONDITION_ACCEPTABLE_ID = str(uuid.uuid4())
CONDITION_NOT_WORKING_ID = str(uuid.uuid4())

ADMIN_ID = str(uuid.uuid4())
USER_ID1 = str(uuid.uuid4())
USER_ID2 = str(uuid.uuid4())
USER_ID3 = str(uuid.uuid4())


ITEM_ID1 = str(uuid.uuid4())
ITEM_ID2 = str(uuid.uuid4())
ITEM_ID3 = str(uuid.uuid4())


items = {
    "id": ITEM_ID1,
    "category_id": CATEGORY_BIKES_ID,
    "user_id": USER_ID1,
    "condition_id": CONDITION_GOOD_ID,
    "title": "Vélo 2 roue motrice",
    "description": "Vend vélo 2 roue motrice en bon état",
}


users = (
    {
        "id": ADMIN_ID,
        "first_name": "Bobby",
        "last_name": "Lemon",
        "nickname": "Bob17",
        "avatar_url": "here.com",
        "email": "hellomail@example.com",
        "password": "notsohashedpassword",
        "phone_number": "0505050505",
    },
    {
        "id": USER_ID1,
        "first_name": "Jean",
        "last_name": "Pierre",
        "nickname": "Pierrot",
        "email": "hello@example.com",
        "password": "notsohashedpassword",
    },
    {
        "id": USER_ID2,
        "first_name": "Mariah",
        "last_name": "Carey",
        "nickname": "AllIWantForChristmas",
        "email": "AllIWantForChristmas@example.com",
        "password": "notsohashedpassword",
    },
    {
        "id": USER_ID3,
        "first_name": "Patrick",
        "last_name": "Camping",
        "nickname": "patoche",
        "email": "patoche@example.com",
        "password": "notsohashedpassword",
    },
)

conditions = (
    {"id": CONDITION_NEW_ID, "label": "New"},
    {"id": CONDITION_LIKENEW_ID, "label": "Like new"},
    {"id": CONDITION_EXCELLENT_ID, "label": "Excellent"},
    {"id": CONDITION_GOOD_ID, "label": "Good"},
    {"id": CONDITION_USED_ID, "label": "Used"},
    {"id": CONDITION_ACCEPTABLE_ID, "label": "Acceptable"},
    {"id": CONDITION_NOT_WORKING_ID, "label": "For parts or not working"},
)

categories = (
    {"id": CATEGORY_CAR_ID, "label": "Car"},
    {"id": CATEGORY_HOUSE_ID, "label": "House"},
    {"id": CATEGORY_JEWELRY_ID, "label": "Jewelry"},
    {"id": CATEGORY_TOOLS_ID, "label": "Tools"},
    {"id": CATEGORY_GAMING_ID, "label": "Video gaming"},
    {"id": CATEGORY_COMPUTER_ID, "label": "Computer"},
    {"id": CATEGORY_BIKES_ID, "label": "Bikes"},
)


DATA_SET = {
    "Categories": categories,
    "Conditions": conditions,
    "Users": users,
    "Items": items,
}

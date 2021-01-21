# pylint: skip-file

"""
Dataset for conditions tests
"""
import uuid

from good_place.db.models import Categories

CATEGORY_CAR_ID = str(uuid.uuid4())
CATEGORY_HOUSE_ID = str(uuid.uuid4())
CATEGORY_JEWELRY_ID = str(uuid.uuid4())
CATEGORY_TOOLS_ID = str(uuid.uuid4())
CATEGORY_GAMING_ID = str(uuid.uuid4())
CATEGORY_COMPUTER_ID = str(uuid.uuid4())
CATEGORY_BIKES_ID = str(uuid.uuid4())


categories = (
    {"id": CATEGORY_CAR_ID, "label": "Car"},
    {"id": CATEGORY_HOUSE_ID, "label": "House"},
    {"id": CATEGORY_JEWELRY_ID, "label": "Jewelry"},
    {"id": CATEGORY_TOOLS_ID, "label": "Tools"},
    {"id": CATEGORY_GAMING_ID, "label": "Video gaming"},
    {"id": CATEGORY_COMPUTER_ID, "label": "Computer"},
    {"id": CATEGORY_BIKES_ID, "label": "Bikes"},
)


DATA_SET = {"Categories": categories}

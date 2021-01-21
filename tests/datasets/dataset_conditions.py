# pylint: skip-file

"""
Dataset for conditions tests
"""
import uuid

from good_place.db.models import Conditions

CONDITION_NEW_ID = str(uuid.uuid4())
CONDITION_LIKENEW_ID = str(uuid.uuid4())
CONDITION_EXCELLENT_ID = str(uuid.uuid4())
CONDITION_GOOD_ID = str(uuid.uuid4())
CONDITION_USED_ID = str(uuid.uuid4())
CONDITION_ACCEPTABLE_ID = str(uuid.uuid4())
CONDITION_NOT_WORKING_ID = str(uuid.uuid4())


conditions = (
    {"id": CONDITION_NEW_ID, "label": "New"},
    {"id": CONDITION_LIKENEW_ID, "label": "Like new"},
    {"id": CONDITION_EXCELLENT_ID, "label": "Excellent"},
    {"id": CONDITION_GOOD_ID, "label": "Good"},
    {"id": CONDITION_USED_ID, "label": "Used"},
    {"id": CONDITION_ACCEPTABLE_ID, "label": "Acceptable"},
    {"id": CONDITION_NOT_WORKING_ID, "label": "For parts or not working"},
)


DATA_SET = {"Conditions": conditions}

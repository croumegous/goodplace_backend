# pylint: skip-file

"""
Dataset for locations tests
"""

import datetime
import uuid

from good_place.db.models import Locations

LOCATION_ID1 = str(uuid.uuid4())
LOCATION_ID2 = str(uuid.uuid4())
LOCATION_ID3 = str(uuid.uuid4())
LOCATION_ID4 = str(uuid.uuid4())
LOCATION_ID5 = str(uuid.uuid4())


locations = (
    {
        "id": LOCATION_ID1,
        "country": "FRA",
        "state": "Haute Garonne",
        "city": "BLAGNAC",
        "street_number": "3",
        "street": "rue des potiers",
        "postal_code": "31700",
    },
    {
        "id": LOCATION_ID2,
        "country": "USA",
        "state": "CA",
        "city": "Fremont",
        "street_number": "43706",
        "street": "Christy St",
        "postal_code": "945383295",
    },
    {
        "id": LOCATION_ID3,
        "country": "FRA",
        "state": "Hérault",
        "city": "MONTPELLIER",
        "street_number": "103",
        "street": "Place Eugène Bataillon",
        "postal_code": "34090",
    },
)


DATA_SET = {"Locations": locations}

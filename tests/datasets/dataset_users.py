# pylint: skip-file

"""
Dataset for users tests
"""

import datetime
import uuid

from good_place.db.models import Locations, Users

ADMIN_ID = str(uuid.uuid4())
USER_ID1 = str(uuid.uuid4())
USER_ID2 = str(uuid.uuid4())
USER_ID3 = str(uuid.uuid4())

LOCATION_ID1 = str(uuid.uuid4())
LOCATION_ID2 = str(uuid.uuid4())
LOCATION_ID3 = str(uuid.uuid4())
LOCATION_ID4 = str(uuid.uuid4())
LOCATION_ID5 = str(uuid.uuid4())


users = (
    {
        "id": ADMIN_ID,
        "first_name": "Bobby",
        "last_name": "Lemon",
        "nickname": "Bob17",
        "avatar_url": "http://here.com",
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


locations = (
    {
        "id": LOCATION_ID1,
        "country": "FRA",
        "state": "Haute Garonne",
        "city": "BLAGNAC",
        "address": "3 rue des potiers",
        "postal_code": "31700",
    },
    {
        "id": LOCATION_ID2,
        "country": "USA",
        "state": "CA",
        "city": "Fremont",
        "address": "43706 Christy St",
        "postal_code": "945383295",
    },
    {
        "id": LOCATION_ID3,
        "country": "FRA",
        "state": "Hérault",
        "city": "MONTPELLIER",
        "address": "Place Eugène Bataillon",
        "postal_code": "34090",
    },
)


DATA_SET = {"Users": users}

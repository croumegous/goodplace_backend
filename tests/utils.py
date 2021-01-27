"""Helper module for running integration tests"""

import uuid

from good_place.core.security import create_jwt_token


def get_header_authentication(user_uuid: uuid.UUID, per_id=None) -> dict:
    """User authentication header for API calls"""
    acces_token = create_jwt_token(user_uuid)
    return {"Authorization": f"Bearer {acces_token}"}

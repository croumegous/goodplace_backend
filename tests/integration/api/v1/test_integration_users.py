import json
from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from good_place.db.models import Users
from tests.datasets.dataset_users import DATA_SET
from tests.fixtures.db import client


@pytest.mark.parametrize("users_data", DATA_SET["Users"])
def test_create_user(client: TestClient, users_data: Dict[str, Any]):
    response = client.post(
        "/api/v1/users", data=json.dumps(users_data), allow_redirects=True
    )
    assert response.status_code == 200

    user_id = users_data.get("id")
    assert Users.exists(id=user_id)
    response = client.get(f"/api/v1/users/{user_id}", allow_redirects=True)
    assert response.status_code == 200

    response = client.delete(f"/api/v1/users/{user_id}", allow_redirects=True)
    assert response.status_code == 200

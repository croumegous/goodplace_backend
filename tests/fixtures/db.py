"""
Config for pytest.
Fixtures added or imported here are available to all tests in subdirectories.
"""
import asyncio
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from good_place.core.settings import CONFIG
from good_place.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    initializer(["good_place.db.models"], db_url=CONFIG.get("DB_DATABASE_URL"))
    with TestClient(app) as c:
        yield c
    finalizer()

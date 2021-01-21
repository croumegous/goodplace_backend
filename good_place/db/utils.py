"""
Init database session
"""

# pylint: disable=no-member
from fastapi.applications import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from good_place.core.settings import CONFIG

TORTOISE_CONFIG = {
    "connections": {"default": CONFIG.get("DB_DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["good_place.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    """
    Initialize database
    """
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )

"""
V1 of good_place API
"""

from fastapi import APIRouter

from . import auth, categories, items, locations, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

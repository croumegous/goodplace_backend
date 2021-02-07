"""
Useful functions for the api
"""

# pylint: disable=no-member
# pylint: disable=no-name-in-module
import re
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from pydantic import BaseModel

from good_place.core.security import ALGORITHM
from good_place.core.settings import CONFIG
from good_place.crud.users import CRUDUser
from good_place.db.models import Users


async def get_current_user(token: str = Depends(HTTPBearer())) -> Optional[Users]:
    """
    Parse the JWT token included in the authorization header and returns a Users object
    which contains information about the currently logged in user

    Args:
        Authorization token
    Returns:
        A Users object or None if unable to find/parse a jwt token
    """
    try:
        payload = jwt.decode(
            token.credentials,
            CONFIG.get("ACCESS_TOKEN_SECRET_KEY"),
            algorithms=ALGORITHM,
        )
        token_id = payload.get("sub")
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=401,
            detail="JWT access_token is expired",
        ) from exc
    except (jwt.JWTError, AttributeError) as exc:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        ) from exc
    user = await CRUDUser.get_user(token_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_admin(
    current_user: Users = Depends(get_current_user),
) -> Optional[Users]:
    """
    Check if current user is admin

    Args:
        current_user (Users): current user
    Raises:
        HTTP error 403 if current user is not admin
    Returns:
        A Users object if user is admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Forbiden user doesn't have enough privileges"
        )

    return current_user


async def verify_refresh_token(refresh_token: str) -> str:
    """Check if refresh token is valid.

    Args:
        refresh_token (str)
    Returns:
        str: the user id of this token
    """
    try:
        payload = jwt.decode(
            refresh_token, CONFIG.get("REFRESH_TOKEN_SECRET_KEY"), algorithms=ALGORITHM
        )
        token_id = payload.get("sub")
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=401,
            detail="JWT refresh_token is expired",
        ) from exc
    except (jwt.JWTError, AttributeError) as exc:
        raise HTTPException(
            status_code=403,
            detail="Could not validate refresh_token",
        ) from exc
    return str(token_id)


def check_sort_field(model: BaseModel, value: str) -> str:
    """Used to parse the "sortField" query parameter
    Check if the provided field is part of model
    Args:
        model (BaseModel): Pydantic model to get available fields
        value (str): the value as a string to be compared with the model
    Raises:
        HTTPException: The provided value is unknown to the model
    Returns:
        str: the initial field value
    """
    value = re.sub(r"(?=[A-Z])", "_", value).lower()  # Convert camel case to snake case
    model_fields = list(model.schema()["properties"])
    # + sign is considered as a space in query so we replace the space to use tortoise order_by
    symbol, fieldname = value[:1].replace(" ", ""), value[1:]

    field = symbol + fieldname

    if fieldname not in model_fields or symbol not in ("", "+", "-"):
        raise HTTPException(status_code=400, detail=f"Incorrect sort field: {field}")

    return field.replace("+", "")

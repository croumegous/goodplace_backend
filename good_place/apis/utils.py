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

from good_place.core.security import ALGORITHM, SECRET_KEY_JWT
from good_place.crud.users import CRUDUser
from good_place.schemas.users import SchemaUser


async def get_current_user(token: str = Depends(HTTPBearer())) -> Optional[SchemaUser]:
    """
    Parse the JWT token included in the authorization header and returns a SchemaUser object
    which contains information about the currently logged in user

    Returns:
        A SchemaUser or None if unable to find/parse a jwt token
    """
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY_JWT, algorithms=ALGORITHM)
        token_id = payload.get("sub")
    except (jwt.JWTError, AttributeError) as exc:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        ) from exc
    user = await CRUDUser.get_user(token_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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

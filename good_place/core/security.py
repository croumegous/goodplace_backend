"""
Useful functions about security
"""
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from good_place.core.settings import CONFIG

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_jwt_token(subject: Union[str, Any], refresh=False) -> str:
    """
    Create a JWT with subject as content

    Args:
        subject(String or Any): The content wich will be set in the JWT
    Returns:
        Strting: Encoded JWT
    """

    if refresh:
        expire = datetime.utcnow() + timedelta(days=CONFIG.get("JWT_EXPIRE_TIME"))
        to_encode = {"exp": expire, "sub": str(subject)}
        return jwt.encode(
            to_encode, CONFIG.get("REFRESH_TOKEN_SECRET_KEY"), algorithm=ALGORITHM
        )

    expire = datetime.utcnow() + timedelta(minutes=CONFIG.get("JWT_EXPIRE_TIME"))
    to_encode = {"exp": expire, "sub": str(subject)}

    return jwt.encode(
        to_encode, CONFIG.get("ACCESS_TOKEN_SECRET_KEY"), algorithm=ALGORITHM
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if plain_password is equal to hashed_password

    Return:
        Boolean: True if password are equivalent, otherwise return False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hashed(password: str) -> str:
    """
    Hash the password in argument

    Args:
        password(String): The password to be hashed
    Return:
        String: the hashed password
    """
    return pwd_context.hash(password)

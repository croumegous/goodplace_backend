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
SECRET_KEY_JWT = CONFIG.get("SECRET_KEY_JWT")


def create_access_token(subject: Union[str, Any]) -> str:
    """
    Create a JWT with subject as content

    Args:
        subject(String or Any): The content wich will be set in the JWT
    Returns:
        Strting: Encoded JWT
    """
    expire = datetime.utcnow() + timedelta(hours=CONFIG.get("JWT_EXPIRE_HOURS"))
    to_encode = {"exp": expire, "sub": str(subject)}

    return jwt.encode(to_encode, SECRET_KEY_JWT, algorithm=ALGORITHM)


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

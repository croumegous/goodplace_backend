"""
All environnement variables
"""
import json
import os

from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "API_V1_STR": os.getenv("API_V1_STR"),
    "DB_ENGINE": os.getenv("DB_ENGINE"),
    "DB_USER": os.getenv("DB_USER"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "DB_HOST": os.getenv("DB_HOST"),
    "DB_PORT": os.getenv("DB_PORT"),
    "DB_DATABASE": os.getenv("DB_DATABASE"),
    "DB_DATABASE_TEST": os.getenv("DB_DATABASE_TEST"),
    "DB_DATABASE_URL": (
        f"{os.getenv('DB_ENGINE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
    ),
    "DB_DATABASE_URL_TEST": (
        f"{os.getenv('DB_ENGINE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE_TEST')}"
    ),
    "MAX_INT_32BITS": int(os.getenv("MAX_INT_32BITS")),
    "SECRET_KEY_JWT": os.getenv("SECRET_KEY_JWT"),
    "JWT_EXPIRE_HOURS": int(os.getenv("JWT_EXPIRE_HOURS")),
    "CORS_ORIGIN": json.loads(os.getenv("CORS_ORIGIN")),
}

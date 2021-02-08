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
    "DB_DATABASE_URL": os.getenv("DATABASE_URL"),
    "DB_DATABASE_URL_TEST": (
        f"{os.getenv('DB_ENGINE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE_TEST')}"
    ),
    "MAX_INT_32BITS": 2_147_483_647,
    "ACCESS_TOKEN_SECRET_KEY": os.getenv("ACCESS_TOKEN_SECRET_KEY"),
    "REFRESH_TOKEN_SECRET_KEY": os.getenv("REFRESH_TOKEN_SECRET_KEY"),
    "JWT_EXPIRE_TIME": int(os.getenv("JWT_EXPIRE_TIME", "15")),
    "CORS_ORIGIN": json.loads(os.getenv("CORS_ORIGIN")),
}

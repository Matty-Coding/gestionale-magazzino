from dotenv import load_dotenv
from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
load_dotenv(BASE_DIR / ".env")

class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_DEV")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


from dotenv import load_dotenv
from os import getenv
from pathlib import Path


# Path corrente + caricamento variabili d'ambiente
BASE_DIR = Path(__file__).parent.resolve()
load_dotenv(BASE_DIR / ".env")

# =========================================================
# ================= Configurazione standard ===============
# =========================================================
class Config:
    SECRET_KEY = getenv("SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SESSION_TYPE = "sqlalchemy"
    SESSION_SERIALIZATION_FORMAT = "json"
    SESSION_PERMANENT = False,

    PERMANENT_SESSION_LIFETIME = 3600   # 1h

# =========================================================
# =============== Configurazione per sviluppo =============
# =========================================================
class DevConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_DEV")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_NAME = "magazzino_session"
    SESSION_COOKIE_SECURE = False

    TEMPLATES_AUTO_RELOAD = True
# =========================================================
# ============== Configurazione per produzione ============
# =========================================================
class ProdConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_NAME = "__Secure-magazzino_session"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


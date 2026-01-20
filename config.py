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
    SESSION_PERMANENT = False

    PERMANENT_SESSION_LIFETIME = 3600  # 1h

    AUTHENTICATION_SALT = getenv("AUTHENTICATION_SALT")
    RESET_PASSWORD_SALT = getenv("RESET_PASSWORD_SALT")

    STRIPE_PUBLIC_KEY = getenv("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = getenv("STRIPE_SECRET_KEY")

    STRIPE_WEBHOOK_SECRET = getenv("STRIPE_WEBHOOK_SECRET")
    
    MAIL_SERVER = getenv("MAIL_SERVER")
    MAIL_PORT = int(getenv("MAIL_PORT"))
    MAIL_USE_TLS = getenv("MAIL_USE_TLS") == "True"
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    MAIL_SUPPRESS_SEND = getenv("MAIL_SUPPRESS_SEND") == "True"
    MAIL_DEFAULT_SENDER = getenv("MAIL_DEFAULT_SENDER")

# =========================================================
# =============== Configurazione per sviluppo =============
# =========================================================
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_DEV")

    SESSION_COOKIE_NAME = "magazzino_session"
    SESSION_COOKIE_SECURE = False


# =========================================================
# ============== Configurazione per produzione ============
# =========================================================
class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_PROD")

    SESSION_COOKIE_NAME = "__Secure-magazzino_session"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

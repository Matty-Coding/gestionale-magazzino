from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_mail import Mail
from flask_limiter.util import get_remote_address


db = SQLAlchemy()

login_manager = LoginManager()

session = Session()

migrate = Migrate()

csrf = CSRFProtect()

talisman = Talisman()

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["60 per minute"]
)

mail = Mail()

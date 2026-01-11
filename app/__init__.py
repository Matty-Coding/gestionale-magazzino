from flask import Flask
from config import DevConfig, ProdConfig, BASE_DIR
from app.extensions import (db, login_manager, session, csrf, talisman, limiter, migrate)
from app.middleware.limit import MiddleWare
from app.models.database import User
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timezone


load_dotenv(BASE_DIR / ".env")

def create_app():
    app = Flask(__name__)

    # =======================================
    # == Configurazione dinamica dev/prod ===
    # =======================================
    if getenv("FLASK_ENV") == "dev":
        app.config.from_object(DevConfig)
    else:
        app.config.from_object(ProdConfig)

    app.config.update(SESSION_SQLALCHEMY=db)

    # ===========================
    # Inizializzazione estensioni
    # ===========================
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    session.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    talisman.init_app(app)
    
    # ===================
    # == LoginManager ===
    # ===================
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Devi effettuare il login per visualizzare questa pagina."

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ============================
    # === Middleware Blocco IP ===
    # ============================
    middleware = MiddleWare()

    @app.before_request
    def check_ip():
        return middleware.check_ip()

    @app.errorhandler(429)
    def ratelimit(e):
        return middleware.limit_handler(e)

    # ==========================
    # === Context processor ====
    # ==========================
    @app.context_processor
    def inject_current_year():
        return {"current_year": datetime.now(timezone.utc).year}

    # ==========================
    # ======  Blueprints  ======
    # ==========================
    from app.blueprints.home.routes import home_bp
    app.register_blueprint(home_bp)

    from app.blueprints.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.cli import create_admin_command
    app.cli.add_command(create_admin_command)

    return app

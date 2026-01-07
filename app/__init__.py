from flask import Flask
from config import DevConfig
from app.extensions import (db, login_manager, session, csrf, talisman, limiter, mail, migrate)
from app.middleware.limit import MiddleWare
from app.models.database import User, IpBloccati


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.config.update(SESSION_SQLALCHEMY=db)

    # ===========================
    # Inizializzazione estensioni
    # ===========================
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    session.init_app(app)
    csrf.init_app(app)
    talisman.init_app(app, content_security_policy={
        "default-src": "'self'",
        "script-src": "'self' https://cdn.jsdelivr.net",
        "style-src": "'self' https://cdn.jsdelivr.net",
        "img-src": "'self'"
    })
    limiter.init_app(app)
    mail.init_app(app)  # pronto per inviare mail

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
        from datetime import datetime, timezone
        return {"current_year": datetime.now(timezone.utc).year}

    # ==========================
    # Blueprint
    # ==========================
    from app.blueprints.home.routes import home_bp
    app.register_blueprint(home_bp)

    return app

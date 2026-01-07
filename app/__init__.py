from app.models.database import db
from flask import Flask
from flask_migrate import Migrate
from config import DevConfig


def create_app():
    # Caricamento app Flask
    app = Flask(__name__)

    # Caricamento configurazione
    app.config.from_object(DevConfig)

    # Inizializzazione database + migrazioni
    db.init_app(app)
    Migrate(app, db)

    return app
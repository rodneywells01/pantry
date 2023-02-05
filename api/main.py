import logging
from math import prod

# logging.basicConfig(level=logging.development)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models.models import db

from routes import healthcheck, inventory, product


logging.basicConfig(level=logging.DEBUG)

def register_blueprints(app):
    app.register_blueprint(healthcheck)
    app.register_blueprint(inventory)
    app.register_blueprint(product)
    return app


def setup():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:postgres@postgres:5432/pantry"  # TODO - do not store here
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    app = register_blueprints(app)

    return app


if __name__ == "__main__":
    print("Starting Pantry")
    app = setup()
    app.run(host="0.0.0.0", port=8080)

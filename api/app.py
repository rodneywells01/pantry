import logging
from math import prod

# logging.basicConfig(level=logging.development)

from flask import Flask

# from flask_migrate import Migrate

from routes import healthcheck, inventory, product


logging.basicConfig(level=logging.DEBUG)

def register_blueprints(app):
    app.register_blueprint(healthcheck)
    app.register_blueprint(inventory)
    app.register_blueprint(product)
    return app


def setup():
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MONGO_URI"] = "mongodb+srv://rodneywells01:WUMNVl6L8Xm3MNPM@pantry-cluster.63imwsx.mongodb.net/?retryWrites=true&w=majority"

    app = register_blueprints(app)

    return app


if __name__ == "__main__":
    print("Starting Pantry")
    app = setup()
    app.run(host="0.0.0.0", port=8080)

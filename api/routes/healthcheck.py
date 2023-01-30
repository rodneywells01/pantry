import logging
from flask import Blueprint

healthcheck = Blueprint('healthcheck', __name__)

@healthcheck.route("/")
def hello_world():
    logging.info("Hello, world!!")
    return "Index Page"


@healthcheck.route("/hello")
def hello():
    logging.info("Hello, world!1")
    return {
        "message": "hello, world!"
    }

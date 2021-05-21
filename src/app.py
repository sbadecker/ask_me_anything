import logging

from flask import Flask, jsonify, request as current_request
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound, Unauthorized

from src import routes
from src.error_handlers import (
    bad_request_400,
    internal_server_error_500,
    not_found_404,
    pydantic_validation_error_400,
    unauthorized_401,
)
from src.logger import setup_logger

logger = logging.getLogger(__name__)


def health_check():
    if current_request.args.get("noisy"):
        logger.debug("this is debug")
        logger.info("this is info")
    return jsonify({"success": True})


def add_url_rules(app):
    app.add_url_rule("/health", "health", health_check)


def register_error_handlers(app):
    app.register_error_handler(Exception, internal_server_error_500)
    app.register_error_handler(ValidationError, pydantic_validation_error_400)
    app.register_error_handler(InternalServerError, internal_server_error_500)
    app.register_error_handler(BadRequest, bad_request_400)
    app.register_error_handler(Unauthorized, unauthorized_401)
    app.register_error_handler(NotFound, not_found_404)


def make_app():
    app = Flask(__name__)

    setup_logger()
    logger.debug("loaded logger")

    logger.debug("registering endpoints...")
    add_url_rules(app)
    logger.debug("registered endpoints!")

    logger.debug("registering error handlers...")
    register_error_handlers(app)
    logger.debug("registered error handlers!")

    return app


app = make_app()


if __name__ == "__main__":
    # for debug only!!
    app.run(host="localhost", port=8000, use_reloader=True)

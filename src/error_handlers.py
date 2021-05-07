import logging

from flask import jsonify
from pydantic import ValidationError

logger = logging.getLogger(__name__)


def internal_server_error_500(err):
    logger.exception("Unhandled error!")
    return jsonify({"success": False, "error": "unhandled error"}), 500


def bad_request_400(err):
    return jsonify({"success": False, "error": "bad request"}), 400


def unauthorized_401(err):
    logger.exception("Unauthorized!")
    return jsonify({"success": False, "error": "unauthorized"}), 401


def not_found_404(err):
    return jsonify({"success": False, "error": "not found"}), 404


def pydantic_validation_error_400(err: ValidationError):
    logger.exception(f"Validation error: {err.json()}")
    return jsonify(err.errors()), 400

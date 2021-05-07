import logging


def setup_logger():
    log_level = logging.DEBUG
    log_format = "{asctime} - {levelname:8s} - {name} - {message}"
    formatter = logging.Formatter(fmt=log_format, style="{")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    handlers = [console_handler]

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = handlers

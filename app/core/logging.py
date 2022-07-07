from logging import DEBUG, Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler
from uuid import uuid4

from flask.logging import default_handler

run_id = uuid4().hex


def get_logger(module):
    # Gets or creates a logger
    logger = getLogger(module)

    # set log level
    logger.setLevel(DEBUG)

    # Stream handler
    stream_handler = StreamHandler()
    stream_formatter = Formatter("%(name)s : %(message)s")
    stream_handler.setFormatter(stream_formatter)

    # File handler
    # roll over after 2KB, and keep backup logs app.log.1, app.log.2 , etc.
    file_handler = RotatingFileHandler(
        f"logs/app-{run_id}.log", maxBytes=200_000, backupCount=5
    )
    file_formatter = Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    file_handler.setFormatter(file_formatter)

    # add file handler to logger
    logger.addHandler(default_handler)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

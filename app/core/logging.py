from logging import DEBUG, Formatter, StreamHandler, getLogger, getLoggerClass
from logging.handlers import RotatingFileHandler


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
    file_handler = RotatingFileHandler("logs/app.log", maxBytes=2000, backupCount=5)
    file_formatter = Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    file_handler.setFormatter(file_formatter)

    # add file handler to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

# logging_example.py
import logging

logger = logging.getLogger(__name__)
logger.propagate = False

if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)

logging.basicConfig()
logger.setLevel(logging.DEBUG)
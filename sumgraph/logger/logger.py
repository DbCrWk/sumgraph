"""
The core logger module for use throughout the application
"""

import logging


handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)


def setup_logger(name: str) -> logging.Logger:
    """
    The function that sets up the logger for a module1
    """
    logger = logging.getLogger(name)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger

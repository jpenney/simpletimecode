from __future__ import absolute_import

from ._compat import NullHandler
import logging


def init_logger(logger_name):
    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        logger.addHandler(NullHandler())
    return logger

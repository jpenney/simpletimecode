from __future__ import absolute_import

import pytest

import simpletimecode.utils


def test_init_logger():
    logger = simpletimecode.utils.init_logger(__name__)
    assert logger.handlers, "should have at least one handler"
    logger.critical('testing')

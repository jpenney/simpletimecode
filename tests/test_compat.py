from __future__ import absolute_import

import pytest

import simpletimecode._compat


@pytest.mark.parametrize("attr", simpletimecode._compat.__all__)
def test_all(attr):
    assert hasattr(simpletimecode._compat, attr)

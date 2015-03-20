from __future__ import absolute_import

import itertools
import re
import sys

import pytest

from simpletimecode import TimeCode
from simpletimecode._compat import (Decimal, decimal_types, integer_types,
                                    string_types)

from .common import TEST_COMBOS


def idfn(val):
    return repr(val)


def _test_convert_to_params():
    for val in set(val for (dummy, dummy, val) in TEST_COMBOS):
        if isinstance(val, string_types) and re.match('\d*\.\d\d\d\d+', val):
            yield pytest.mark.xfail(val)
        else:
            yield val


@pytest.mark.parametrize("val", _test_convert_to_params())
def test_convert_to(val):
    #     if isinstance(val, string_types) and re.match('\d*\.\d\d\d\d+', val):
    #         pytest.skip("too many decimal places: %s" % val)
    assert isinstance(TimeCode(val), TimeCode)


def _test_roundtrip_params():
    fail_types = string_types + decimal_types + (float,)
    for entry in TEST_COMBOS:
        if entry[0] in fail_types:
            yield pytest.mark.xfail(entry)
        else:
            yield entry


@pytest.mark.parametrize("typ, orig, val", _test_roundtrip_params())
def test_roundtrip(typ, orig, val):
    #     if typ in string_types + decimal_types + (float,):
    #         pytest.skip("round tripping not supported for %s" % typ)
    assert typ(TimeCode(val)) == val


@pytest.mark.parametrize("typ, val", set((typ, val)
                                         for (typ, dummy, val) in TEST_COMBOS))
def test_as_seconds(typ, val):
    assert TimeCode(val).as_seconds() == Decimal('%s' % val)


@pytest.mark.parametrize(
    "input", (pytest.mark.xfail(i, raises=TypeError)
              for i in ('1:00.0011', '1 hour', '0.000007')))
def test_invalid_conversion_from_tcode(input):
    tcode = TimeCode.from_tcode(input)


@pytest.mark.parametrize(
    "input", (pytest.mark.xfail(i, raises=TypeError)
              for i in ((1, 2), '1 hour', '')))
def test_invalid_conversion_constructor(input):
    tcode = TimeCode(input)

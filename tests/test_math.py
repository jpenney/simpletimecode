from __future__ import absolute_import

import itertools
import math
import operator
import sys

import pytest

from simpletimecode import TimeCode
from simpletimecode._compat import Decimal

VALS = (1, 1.159007, Decimal('1.815'), sys.maxsize + 1)


@pytest.mark.parametrize("inp, places", itertools.product(VALS, range(3)))
def test_round(inp, places):

    tcval = TimeCode(inp)
    tcrslt = round(tcval, places)
    rslt = round(inp, places)
    msg = (
        "round(%(tcval)r, %(places)r) => %(tcrslt)r != "
        "round(%(inp)r, %(places)r) => %(rslt)r" % dict(
            tcval=tcval, places=places, tcrslt=tcrslt, inp=inp, rslt=rslt))
    # handle python version differences
    assert tcrslt == rslt or tcrslt == TimeCode('%s' % rslt), msg


@pytest.mark.parametrize("inp", VALS)
def test_floor(inp):
    tcval = TimeCode(inp)
    tcrslt = math.floor(tcval)
    rslt = math.floor(inp)
    msg = (
        "math.floor(%(tcval)r) => %(tcrslt)r != "
        "math.floor(%(inp)r) => %(rslt)r" % dict(
            tcval=tcval, tcrslt=tcrslt, inp=inp, rslt=rslt))
    assert tcrslt == rslt, msg


@pytest.mark.parametrize("inp", VALS)
def test_ceil(inp):
    tcval = TimeCode(inp)
    tcrslt = math.ceil(tcval)
    rslt = math.ceil(inp)
    msg = (
        "math.ceil(%(tcval)r) => %(tcrslt)r != "
        "math.ceil(%(inp)r) => %(rslt)r" % dict(
            tcval=tcval, tcrslt=tcrslt, inp=inp, rslt=rslt))
    assert tcrslt == rslt, msg


@pytest.mark.parametrize(
    "oper_name, a, b, expected",
    (('add', TimeCode('1:00'), TimeCode('1:00:00'), TimeCode('1:01:00')),
     ('sub', TimeCode('10:00:01.01'), 1, TimeCode('10:00:00.01')),
     ('mul', TimeCode('1111:11:11.11'), 2, TimeCode('2222:22:22.22')),
     ('mul', TimeCode(60), 2, TimeCode('2:00')),
     ('truediv', TimeCode(60 * 60), 2, TimeCode('30:00'))))
def test_math_ops(oper_name, a, b, expected):
    oper = getattr(operator, oper_name)
    assert oper(a, b) == expected

from __future__ import absolute_import

import itertools
import operator
import sys

import pytest

from simpletimecode import TimeCode
from simpletimecode._compat import (Decimal, decimal_types, integer_types,
                                    string_types)

from .test_conversions import TEST_COMBOS

OPERATIONS = dict(
    abs=('1op', 'math'),
    add=('2op', 'math'),
    and_=('2op', 'bitwise'),
    concat=('2op', 'sequence'),
    contains=('2op', 'sequence'),
    countOf=('2op', 'sequence'),
    delitem=('2op', 'sequence'),
    div=('2op', 'math'),
    eq=('2op', 'logic'),
    floordiv=('2op', 'math'),
    ge=('2op', 'logic'),
    getitem=('2op', 'sequence'),
    gt=('2op', 'logic'),
    iadd=('inplace', 'math'),
    iand=('inplace', 'bitwise'),
    iconcat=('inplace', 'sequence'),
    idiv=('inplace', 'math'),
    ifloordiv=('inplace', 'math'),
    ilshift=('inplace', 'bitwise'),
    imod=('inplace', 'math'),
    imul=('inplace', 'math'),
    index=('1op', 'sequence'),
    indexOf=('2op', 'sequence'),
    invert=('1op', 'bitwise'),
    ior=('inplace', 'bitwise'),
    ipow=('inplace', 'math'),
    irshift=('inplace', 'bitwise'),
    is_=('2op', 'logic'),
    is_not=('2op', 'logic'),
    isub=('inplace', 'math'),
    itruediv=('inplace', 'math'),
    ixor=('inplace', 'bitwise'),
    le=('2op', 'logic'),
    lshift=('2op', 'bitwise'),
    lt=('2op', 'logic'),
    mod=('2op', 'math'),
    mul=('2op', 'math'),
    ne=('2op', 'logic'),
    neg=('1op', 'math'),
    not_=('1op', 'logic'),
    or_=('2op', 'bitwise'),
    pos=('1op', 'math'),
    pow=('2op', 'math'),
    rshift=('2op', 'bitwise'),
    setitem=('2op', 'sequence'),
    sub=('2op', 'math'),
    truediv=('2op', 'math'),
    truth=('1op', 'logic'),
    xor=('2op', 'bitwise'))

VALUES_1OP = [entry[2] for entry in TEST_COMBOS]
VALUES_1OP += list(set(TimeCode(i) for i in VALUES_1OP))
VALUES_2OP = set(itertools.combinations(VALUES_1OP, 2))


def _test_unsupported_op_params():
    unsupported_types = ('bitwise', 'sequence')
    for oper_name in OPERATIONS:
        oper_args, oper_type = OPERATIONS[oper_name]
        if oper_type in unsupported_types:
            yield pytest.mark.xfail((oper_type, oper_args, oper_name),
                                    raises=TypeError)


def _test_supported_1op_params():
    no_float = ('pos', 'neg', 'abs')
    ops = (
        (oper_type, oper_args, oper_name)
        for (oper_name, (oper_args, oper_type))
        in OPERATIONS.items()
        if oper_args == '1op' and oper_type not in ('bitwise', 'sequence'))
    for ((oper_type, oper_args, oper_name), val) in itertools.product(
            ops, VALUES_1OP):
        if isinstance(val, float) and oper_name in no_float:
            continue
        if isinstance(val, string_types) and Decimal(val) == 0:
            continue
        else:
            try:
                oper = getattr(operator, oper_name)
                dummy = oper(val)
                yield oper_type, oper_name, val
            except Exception:
                pass


def _test_supported_2op_params():
    skip_types = string_types + (float,)
    ops = (
        (oper_type, oper_args, oper_name)
        for (oper_name, (oper_args, oper_type))
        in OPERATIONS.items()
        if oper_args != '1op' and oper_type not in ('bitwise', 'sequence'))
    for ((oper_type, oper_args, oper_name), (val1, val2)) in itertools.product(
            ops, VALUES_2OP):
        if (isinstance(val1, skip_types) or
                isinstance(val2, skip_types)):
            continue
        xfail = False
        if oper_type == 'math':

            if ('pow' in oper_name and val1 == val2 and Decimal(val1) == 0):
                xfail = True
        if oper_type == 'logic' and oper_name.startswith('is_'):
            # TODO: test 'is_' / 'is_not' separately
            continue
        try:
            oper = getattr(operator, oper_name)
            dummy = oper(val1, val2)
            if xfail:
                yield pytest.mark.xfail((oper_type, oper_name, val1, val2))
            else:
                yield oper_type, oper_name, val1, val2
        except Exception:
            pass


def _test_mixed_math_params():
    math_skip_types = string_types + (float,)

    ops = (
        (oper_type, oper_args, oper_name)
        for (oper_name, (oper_args, oper_type))
        in OPERATIONS.items()
        if oper_args != '1op' and oper_type not in ('bitwise', 'sequence'))
    for ((oper_type, oper_args, oper_name), (val1, val2)) in itertools.product(
            ops, VALUES_2OP):
        xfail = False
        if oper_type == 'math':
            if (isinstance(val1, math_skip_types) or
                    isinstance(val2, math_skip_types)):
                continue
            if ('pow' in oper_name and val1 == val2 and Decimal(val1) == 0):
                xfail = True

        try:
            oper = getattr(operator, oper_name)
            dummy = oper(val1, val2)
            if xfail:
                yield pytest.mark.xfail((oper_type, oper_name, val1, val2))
            else:
                yield oper_type, oper_name, val1, val2
        except Exception:
            pass


@pytest.mark.parametrize(
    "oper_type, oper_args, oper_name", _test_unsupported_op_params())
def test_unsupported_op(oper_type, oper_args, oper_name):
    dummy = oper_type
    oper = getattr(operator, oper_name)
    if oper_args == '1op':
        oper(TimeCode(0))
    else:
        oper(TimeCode(1), TimeCode(2))


@pytest.mark.parametrize(
    "oper_type, oper_name, val", _test_supported_1op_params())
def test_supported_1op(oper_type, oper_name, val):
    oper = getattr(operator, oper_name)
    item = TimeCode(val)
    orig_result = oper(val)
    tc_result = oper(item)
    assert orig_result == tc_result, (
        "operator.%(oper_name)s(%(val)r) => %(orig_result)r != "
        "operator.%(oper_name)s(%(item)r) => %(tc_result)r" % dict(
            oper_name=oper_name, val=val, item=item,
            orig_result=orig_result, tc_result=tc_result))


@pytest.mark.parametrize(
    "oper_type, oper_name, val1, val2", _test_supported_2op_params())
def test_supported_2op(oper_type, oper_name, val1, val2):
    oper = getattr(operator, oper_name)
    if oper_type == 'math':
        division = 'div' in oper_name or 'mod' in oper_name
        try:
            orig_result = oper(val1, val2)
        except Exception as err:
            pytest.skip("%s" % err)

        tc1 = TimeCode(val1)
        tc2 = TimeCode(val2)
        tc_result = oper(tc1, tc2)
        orig_result = oper(val1, val2)
        tc_comp = TimeCode(orig_result)
        if not division:
            try:
                msg = (
                    "operator.%(oper_name)s(%(tc1)r, %(tc2)r) => "
                    "%(tc_result)r != "
                    "TimeCode(operator.%(oper_name)s(%(val1)r, %(val2)r) => "
                    "TimeCode(%(orig_result)r) => %(tc_comp)r" % dict(
                        oper_name=oper_name, tc1=tc1, tc2=tc2,
                        tc_result=tc_result, val1=val1, val2=val2,
                        orig_result=orig_result, tc_comp=tc_comp))
            except Exception as err:
                msg = "error building message: %s" % err
            assert tc_result == tc_comp, msg
        else:
            try:
                msg = (
                    "str(operator.%(oper_name)s(%(tc1)r, %(tc2)r)) => "
                    "str(%(tc_result)r) => '%(tc_result)s' != "
                    "str(TimeCode(operator.%(oper_name)s(%(val1)r, "
                    "%(val2)r)) => "
                    "str(TimeCode(%(orig_result)r)) => str(%(tc_comp)r) => "
                    "'%(tc_comp)s'" % dict(
                        oper_name=oper_name, tc1=tc1, tc2=tc2,
                        tc_result=tc_result, val1=val1, val2=val2,
                        orig_result=orig_result, tc_comp=tc_comp))
            except Exception as err:
                msg = "error building message: %s" % err
            assert str(tc_result) == str(tc_comp), msg

    elif oper_type == 'logic':
        orig_result = oper(val1, val2)
        tc1 = TimeCode(val1)
        tc2 = TimeCode(val2)
        tc_result = oper(tc1, tc2)
        try:
            msg = (
                "operator.%(oper_name)s(%(tc1)r, %(tc2)r)) => "
                "operator.%(oper_name)s(%(tc1_sec)r, %(tc2_sec)r)) => "
                "%(tc_result)r != "
                "operator.%(oper_name)s(%(val1)r, %(val2)r) => "
                "%(orig_result)r")
            msg = msg % dict(
                oper_name=oper_name, val1=val1, val2=val2, tc1=tc1, tc2=tc2,
                orig_result=orig_result, tc_result=tc_result,
                tc1_sec=tc1.as_seconds(), tc2_sec=tc2.as_seconds())
        except Exception as err:
            msg = "error building message: %s" % err
        assert tc_result == orig_result, msg

    else:
        assert False, "unexpected oper_type=%s" % oper_type

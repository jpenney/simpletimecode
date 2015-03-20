#!/usr/bin/env python


from simpletimecode import TimeCode
from simpletimecode._compat import (
    Decimal, decimal_types, integer_types,
    string_types, integer_types)
import itertools

import pytest

import operator


def _iter_type_value(combos):
    for (typ, val) in combos:
        try:
            yield (typ, val, typ(val))
        except ValueError:
            pass
    raise StopIteration()

TEST_TYPES = [float] + list(decimal_types + integer_types + string_types)
# 315360000 == 10 years
TEST_VALUES = [0, 0.1, 1, 1.0000001, 315360000, -1, -2.0,
               '0', '0.1', '1', '1.0000001', '315360000', '-1', '-2.0']

TEST_COMBOS = set(_iter_type_value(
    itertools.product(TEST_TYPES, TEST_VALUES)))

VALUES_1OP = [entry[2] for entry in TEST_COMBOS]
VALUES_1OP += list(set(TimeCode(i) for i in VALUES_1OP))
VALUES_2OP = list(itertools.combinations(VALUES_1OP, 2))


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

UNSUPPORTED_OP_TYPES = ('bitwise', 'sequence')


def get_argmap_1op():
    for oper_name in OPERATIONS:
        oper_args, oper_type = OPERATIONS[oper_name]
        if oper_args == '1op' and hasattr(
                operator, oper_name) and oper_type not in UNSUPPORTED_OP_TYPES:
            for val in VALUES_1OP:
                yield (oper_type, oper_args, oper_name, val)


def get_argmap_2op():
    for oper_name in OPERATIONS:
        oper_args, oper_type = OPERATIONS[oper_name]
        if oper_args != '1op' and hasattr(
                operator, oper_name) and oper_type not in UNSUPPORTED_OP_TYPES:
            for (val1, val2) in VALUES_2OP:
                yield (oper_type, oper_args, oper_name, val1, val2)


def get_unsupported_ops():
    for oper_name in OPERATIONS:
        oper_args, oper_type = OPERATIONS[oper_name]
        if oper_type in UNSUPPORTED_OP_TYPES and hasattr(
                operator, oper_name):
            yield oper_type, oper_args, oper_name


def get_1op_test_params():
    skip_types = (float,) + string_types
    no_skip_types = ('pos', 'neg', 'abs')
    for (oper_type, oper_args, oper_name, val) in get_argmap_1op():
        if isinstance(val, skip_types) and oper_name in no_skip_types:
            continue
        if isinstance(val, string_types) and Decimal('%s' % val) == 0:
            continue
        yield oper_type, oper_name, val


def get_2op_test_params():
    skip_types = string_types + (float,)
    skip = []
    for (oper_type, oper_args, oper_name, val1, val2) in get_argmap_2op():
        # avoid mixed decimal math/logic
        if (isinstance(val1, decimal_types) and
                isinstance(val2, decimal_types) and
                type(val1) != type(val2)):
            continue

        # skip types
        if isinstance(val1, skip_types) or isinstance(val2, skip_types):
            continue

        if oper_type == 'logic':
            if oper_name.startswith('is_'):
                continue

        if oper_type == 'math':
            if val2 == 0 and ('mod' in oper_name or 'div' in oper_name):
                continue
            if 'pow' in oper_name:
                if val1 < 0 and not isinstance(val2, integer_types):
                    continue
                if val1 == val2 and 0 == (
                        val1 if isinstance(val1, decimal_types)
                        else Decimal(val1)):
                    continue
                if abs(val1) > 1000 or abs(val2) > 1000:
                    continue
                if val1 == 0 and val2 < 0:
                    continue
            if 'floordiv' in oper_name and (
                isinstance(val1, decimal_types) or
                isinstance(val2, decimal_types)) and (
                    val1 < 1 or val2 < 1):
                # Decimal floordiv  seems non-standard with
                # negative numbers marking xfail until
                # I can investigate further
                yield pytest.mark.xfail((oper_type, oper_name, val1, val2))
                continue
            if 'mod' in oper_name and (
                isinstance(val1, integer_types) or
                isinstance(val2, integer_types)) and (
                    (val1 * val2) < 0):
                # Decimal mod seems non-standard with
                # mixed sign numbers marking xfail until
                # I can investigate further
                yield pytest.mark.xfail((oper_type, oper_name, val1, val2))
                continue

            yield (oper_type, oper_name, val1, val2)

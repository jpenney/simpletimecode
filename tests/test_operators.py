from __future__ import absolute_import, division

import itertools
import operator
import sys

import pytest
import _pytest

from simpletimecode import TimeCode
from simpletimecode._compat import (Decimal, decimal_types, integer_types,
                                    string_types)

from .common import (
    get_unsupported_ops, get_1op_test_params, get_2op_test_params)

#
# def _test_unsupported_op_params():
#     unsupported_types = ('bitwise', 'sequence')
#     for oper_name in OPERATIONS:
#         oper_args, oper_type = OPERATIONS[oper_name]
#         if oper_type in unsupported_types:
#             yield pytest.mark.xfail((oper_type, oper_args, oper_name),
#                                     raises=TypeError)
#
#
# def _test_supported_1op_params():
#     no_float = ('pos', 'neg', 'abs')
#     ops = (
#         (oper_type, oper_args, oper_name)
#         for (oper_name, (oper_args, oper_type))
#         in OPERATIONS.items()
#         if oper_args == '1op' and oper_type not in ('bitwise', 'sequence'))
#     for ((oper_type, oper_args, oper_name), val) in itertools.product(
#             ops, VALUES_1OP):
#         if isinstance(val, float) and oper_name in no_float:
#             continue
#         if isinstance(val, string_types) and Decimal('%s' % val) == 0:
#             continue
#
#         try:
#             oper = getattr(operator, oper_name)
#             dummy = oper(val)
#             yield oper_type, oper_name, val
#         except Exception:
#             pass
#
#
# def _test_supported_2op_params():
#     skip_types = string_types + (float,)
#     ops = list(
#         (oper_type, oper_args, oper_name)
#         for (oper_name, (oper_args, oper_type))
#         in OPERATIONS.items()
#         if oper_args != '1op' and oper_type not in ('bitwise', 'sequence')
#         and oper_name not in ('is_', 'is_not'))
#     vals = list((val1, val2) for (val1, val2) in VALUES_2OP if not (
#         (isinstance(val1, skip_types) or
#          isinstance(val2, skip_types))))
#
#     params = list((oper + vals)
#                   for (oper, vals) in itertools.product(ops, vals))
#
#     for (oper_type, oper_args, oper_name, val1, val2) in params:
#         idstr = "%r %r %r %r %r" % (
#             oper_type, oper_args, oper_name, val1, val2)
#
#         if (isinstance(val1, decimal_types) and
#                 isinstance(val2, decimal_types) and
#                 type(val1) != type(val2)):
# avoid mixed decimal math/logic
#             print "%s: mixed decimal" % idstr
#             continue
#
#         if oper_type == 'logic':
#             if oper_name.startswith('is_'):
# TODO: test is_/is_not separately
#                 print "%s: is_/is_not" % idstr
#                 continue
#
#         if oper_type == 'math':
#             if val2 == 0 and ('mod' in oper_name or 'div' in oper_name):
#                 print "%s: divide by zero" % idstr
#                 continue
#
#         print "%s: OK" % idstr
#         yield oper_type, oper_name, val1, val2
#     print "ops=%d, vals=%d, params=%d" % (len(ops), len(vals), len(params))
#     raise StopIteration
#     params2 = (
#         (oper_type, oper_args, oper_name, val1, val2) for
#         (oper_type, oper_args, oper_name, val1, val2) in params
#         if not (
#             ('pow' in oper_name and abs(val1) > 1000 and abs(val2) > 1000)
#             or
#             (oper_type == 'logic' and (
#                 oper_name.startswith('is_') or (
#                     isinstance(val1, decimal_types) and
#                     isinstance(val2, decimal_types) and
#                     type(val1) != type(val2))))))
#
#     for (oper_type, oper_args, oper_name, val1, val2) in params2:
#         print "%r %r %r %r %r" % (oper_type, oper_args, oper_name, val1, val2)
#         try:
#             oper = getattr(operator, oper_name)
#             dummy = oper(val1, val2)
#             yield oper_type, oper_name, val1, val2
#         except Exception as err:
#             print "%r" % err
#             pass
#     raise StopIteration
#     x = 0
#     for (oper_type, oper_args, oper_name, val1, val2) in params:
# for ((oper_type, oper_args, oper_name), (val1, val2)) in itertools.product(
# ops, vals):
#         x += 1
#         xfail = False
#         if oper_type == 'math':
#             if 'pow' in oper_name:
#                 if val1 == val2 and 0 == (
#                         val1 if isinstance(val1, decimal_types)
#                         else Decimal(val1)):
#                     xfail = True
#
#                 if (abs(val1) > 1000 and val2 < 0) or (
#                         abs(val2) > 1000 and val1 < 0):
# likely to overflow
#                     xfail = True
#
#         if oper_type == 'logic':
#             if oper_name.startswith('is_'):
# TODO: test 'is_' / 'is_not' separately
#                 continue
#             if (isinstance(val1, decimal_types) and
#                     isinstance(val2, decimal_types) and
#                     type(val1) != type(val2)):
# avoid mixing cdecimal/decimal
#                 continue
#         try:
#             oper = getattr(operator, oper_name)
#             dummy = oper(val1, val2)
#             if xfail:
#                 print "%10d: yield xfail" % x
#                 yield pytest.mark.xfail((oper_type, oper_name, val1, val2))
#             else:
#                 print "%10d: yield" % x
#                 yield oper_type, oper_name, val1, val2
#         except Exception:
#             print "%10d: whoops" % x
#             pass
#
#
# def _test_mixed_math_params():
#     math_skip_types = string_types + (float,)
#
#     ops = (
#         (oper_type, oper_args, oper_name)
#         for (oper_name, (oper_args, oper_type))
#         in OPERATIONS.items()
#         if oper_args != '1op' and oper_type not in ('bitwise', 'sequence'))
#     for ((oper_type, oper_args, oper_name), (val1, val2)) in itertools.product(
#             ops, VALUES_2OP):
#         xfail = False
#         if oper_type == 'math':
#             if (isinstance(val1, math_skip_types) or
#                     isinstance(val2, math_skip_types)):
#                 continue
#             if ('pow' in oper_name and val1 == val2 and Decimal(val1) == 0):
#                 xfail = True
#
#         try:
#             oper = getattr(operator, oper_name)
#             dummy = oper(val1, val2)
#             if xfail:
#                 yield pytest.mark.xfail((oper_type, oper_name, val1, val2))
#             else:
#                 yield oper_type, oper_name, val1, val2
#         except Exception:
#             pass


@pytest.mark.parametrize(
    "oper_type, oper_args, oper_name", get_unsupported_ops())
def test_unsupported_op(oper_type, oper_args, oper_name):
    dummy = oper_type
    oper = getattr(operator, oper_name)
    if oper_args == '1op':
        try:
            oper(TimeCode(0))
        except Exception:
            return
    else:
        try:
            oper(TimeCode(1), TimeCode(2))
        except Exception:
            return

    assert False, "operation should not have worked: %s" % oper_name


@pytest.mark.parametrize(
    "oper_type, oper_name, val", get_1op_test_params())
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
    "oper_type, oper_name, val1, val2", get_2op_test_params())
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
            if oper_name in ('div', 'idiv') and oper(
                float(val1), float(val2)) < 1 and (
                    isinstance(val1, integer_types) or
                    isinstance(val2, integer_types)):
                # interger math is inexact
                assert (tc_comp - 1) < tc_result < (tc_comp + 1)
            else:
                try:
                    msg = (
                        "str(operator.%(oper_name)s(%(tc1)r, %(tc2)r)) => "
                        "str(%(tc_result)r) => '%(tc_result)s' != "
                        "str(TimeCode(operator.%(oper_name)s(%(val1)r, "
                        "%(val2)r)) => "
                        "str(TimeCode(%(orig_result)r)) => "
                        "str(%(tc_comp)r) => "
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

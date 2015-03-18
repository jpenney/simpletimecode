from __future__ import absolute_import

import math
import numbers
import operator
import re

from ._compat import Decimal, string_types, total_ordering, decimal_types


@total_ordering
class TimeCode(numbers.Real):

    TS_RE_STR = (r'^[+-]?(([0-9]+:[0-9]{2}|[0-9]+):[0-9]{2}|[0-9]+)'
                 r'(.[0-9]{1,3}0*)?$')
    TS_RE = re.compile(TS_RE_STR)

    def __init__(self, num=0):
        super(TimeCode, self).__init__()
        if isinstance(num, decimal_types):
            self._seconds = Decimal(num.as_tuple())
        else:
            self._seconds = self._convert_other(num)._seconds

    @classmethod
    def from_tcode(cls, tstamp):
        tstamp = tstamp.strip().lstrip('+')
        sign = 1
        if tstamp[0] == '-':
            sign = -1
            tstamp = tstamp[1:]
        if cls.TS_RE.match(tstamp):
            (hours, mins, secs) = (([0] * 3) + tstamp.split(':'))[-3:]
            return cls((((int(hours) * 60) + int(mins)) * 60)
                       + Decimal(secs) * sign)
        else:
            raise TypeError("%r is not a valid TimeCode format" % tstamp)

    def as_tuple(self):
        sign = 1 if self < 0 else 0
        mins, secs = divmod(abs(self._seconds), 60)
        hours, mins = divmod(mins, 60)
        return (sign, int(hours), int(mins), secs)

    def as_tcode(self):
        sign, hours, mins, secs = self.as_tuple()
        return "%s%02d:%02d:%06.3f" % ('-' if sign else '', hours, mins, secs)

    def as_seconds(self):
        return self._seconds

    def _do_operation2(self, other, operation):
        other = self._convert_other(other)
        if other is NotImplemented:
            return other
        try:
            result = operation(self._seconds, other._seconds)
        except TypeError:
            result = NotImplemented
        if result is NotImplemented:
            return result
        return self._convert_other(result)

    def _do_reverse_operation2(self, other, operation):
        other = self._convert_other(other)
        if other is NotImplemented:
            return other
        try:
            return operation(other, self)
        except TypeError:
            return NotImplemented

    def __str__(self):
        return self.as_tcode()

    @classmethod
    def _convert_other(cls, other):
        if isinstance(other, TimeCode):
            return other
        elif isinstance(other, Decimal):
            return TimeCode(other)
        elif isinstance(other, string_types):
            if cls.TS_RE.match(other):
                return cls.from_tcode(other)
            else:
                try:
                    return TimeCode(Decimal(other))
                except Exception:
                    pass
        elif isinstance(other, numbers.Number):
            return TimeCode(Decimal(str(other)))

        raise TypeError("Unable to convert %r to %s" % (other, cls))

    def __repr__(self):
        return "TimeCode('%s')" % self

    def __hash__(self):
        return hash(self._seconds)

    def __abs__(self):
        return TimeCode(operator.abs(self._seconds))

    def __neg__(self):
        return TimeCode(operator.neg(self._seconds))

    def __pos__(self):
        return TimeCode(operator.pos(self._seconds))

    def __float__(self):
        return float(self._seconds)

    def __trunc__(self):
        return int(self._seconds)

    def __eq__(self, other):
        return self._seconds == other

    def __lt__(self, other):
        return self._seconds < other

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ceil__(self):
        return math.ceil(self._seconds)

    def __floor__(self):
        return math.floor(self._seconds)

    def __round__(self, *args):
        rslt = round(self._seconds, *args)
        if isinstance(rslt, decimal_types):
            # result type depends on pyhon version
            return TimeCode(rslt)
        else:
            return rslt

    # 2ops
    def __add__(self, other):
        return self._do_operation2(other, operator.add)

    def __radd__(self, other):
        return self._do_reverse_operation2(other, operator.add)

    def __sub__(self, other):
        return self._do_operation2(other, operator.sub)

    def __rsub__(self, other):
        return self._do_reverse_operation2(other, operator.sub)

    def __div__(self, other):
        return self._do_operation2(other, operator.div)

    def __rdiv__(self, other):
        return self._do_reverse_operation2(other, operator.div)

    def __floordiv__(self, other):
        return self._do_operation2(other, operator.floordiv)

    def __rfloordiv__(self, other):
        return self._do_reverse_operation2(other, operator.floordiv)

    def __mod__(self, other):
        return self._do_operation2(other, operator.mod)

    def __rmod__(self, other):
        return self._do_reverse_operation2(other, operator.mod)

    def __mul__(self, other):
        return self._do_operation2(other, operator.mul)

    def __rmul__(self, other):
        return self._do_reverse_operation2(other, operator.mul)

    def __pow__(self, other):
        return self._do_operation2(other, operator.pow)

    def __rpow__(self, other):
        return self._do_reverse_operation2(other, operator.pow)

    def __truediv__(self, other):
        return self._do_operation2(other, operator.truediv)

    def __rtruediv__(self, other):
        return self._do_reverse_operation2(other, operator.truediv)

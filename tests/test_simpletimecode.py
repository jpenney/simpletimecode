import math

from simpletimecode import TimeCode
from simpletimecode._compat import Decimal


def test_timecode():
    tc_zero = TimeCode(0)
    assert tc_zero == 0
    assert tc_zero.as_tuple() == (0, 0, 0, 0)
    assert tc_zero.as_seconds() == Decimal('0')
    assert tc_zero.as_tcode() == '00:00:00.000'
    math.floor(tc_zero)
    math.ceil(tc_zero)
    round(tc_zero)

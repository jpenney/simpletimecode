import sys

# flake8: noqa

__all__ = [
    'PY2', 'text_type', 'string_types', 'integer_types', 'Decimal',
    'decimal_types', 'total_ordering']

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
else:
    text_type = str
    string_types = (str,)
    integer_types = (int, )

try:
    from cdecimal import Decimal
    import decimal
    decimal_types = (Decimal, decimal.Decimal)
except ImportError:
    from decimal import Decimal
    decmial_types = (Decimal,)

try:
    from functools import total_ordering
except ImportError:
    from total_ordering import total_ordering

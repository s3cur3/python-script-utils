import re
from typing import Iterable, Any


def quoted(stringlike):
    return '"%s"' % stringlike

def compress_spaces(line: str) -> str:
    """Compresses all instances of multiple whitespace in a row down to a single space"""
    return re.sub(r'\s+', ' ', line).strip() + '\n'

def print_all(stringlikes: Iterable[Any], prefix='', suffix='\n'):
    for s in stringlikes:
        print('%s%s' % (prefix, s), end=suffix)

def format_float(n: float, decimals: int=8) -> str:
    """
    A float-to-string converter that works like Python's 'g' formatting mode
    (https://docs.python.org/3/library/string.html#format-specification-mini-language),
    except that it never gives you scientific notation.

    If you need a yet faster version, you can reimplement this with a fixed decimal precision.
    (The string interpolation of the decimal argument adds ~33% to this function's runtime.

    Credit to Ted Greene for optimizing this a ton.

    >>> format_float(1.00000016)
    '1.0000002'
    >>> format_float(1.000000000000001)
    '1'
    >>> format_float(100000000000.1)
    '100000000000.1000061'
    """
    s = f"{n:.{decimals}g}"
    if "e" in s:
        return f"{n:.{decimals}f}".rstrip('0').rstrip('.')
    return s

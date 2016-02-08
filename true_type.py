"""
Returns real type of a string
>>> get_type('2010/1/12')
<type 'datetime.datetime'>
>>> get_type('2010.2')
<type 'float'>
>>> get_type('2010')
<type 'int'>
>>> get_type('2013test')
<type 'str'>
"""
from datetime import datetime

tests = [
    # (Type, Test)
    (int, int),
    (float, float),
    (datetime, lambda value: datetime.strptime(value, "%Y/%m/%d"))
]

def get_type(value):
    """
    value : any value or variable containing string whose true type is required
    returns true type of the string
    example get_type('5') -> int
    """
    for typ, test in tests:
        try:
            test(value)
            return typ
        except ValueError:
            continue
    # No match
    return str


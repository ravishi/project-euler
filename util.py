import string

def itoa(n, base=10, numerals=string.digits+string.ascii_lowercase):
    """
    Converts any number to any base.

        >>> itoa(8, 2)
        '1000'
        >>> itoa(16, 2)
        '10000'
    """
    return not n and '0' or itoa(n // base, base, numerals).lstrip('0') + numerals[n % base]

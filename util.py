import string
import math

def gcd(a, b):
    """
    Greatest common divisor.::

        >>> gcd(48, 180)
        12
    """
    return a if b == 0 else gcd(b, a % b)


def lcm(a, b):
    """
    Least common multiple.::

        >>> lcm(4, 6)
        12
        >>> reduce(lcm, (8, 9, 21))
        504
    """
    return abs(a * b) / gcd(a, b)


def itoa(n, base=10, numerals=string.digits+string.ascii_lowercase):
    """
    Converts any number to any base.

    FIXME 'any' to 'any', really?

        >>> itoa(8, 2)
        '1000'
        >>> itoa(16, 2)
        '10000'
    """
    return not n and '0' or itoa(n // base, base, numerals).lstrip('0') + numerals[n % base]


def primegen():
    """
    A simple prime generator. We can assert its ok based on the
    solution of problem 07.::

        >>> g = primegen()
        >>> next(g)
        2
        >>> next(g)
        3
        >>> [next(g) for i in xrange(5)][-1] # the 7th prime
        17
        >>> [next(g) for i in xrange(10001 - 7)][-1] # the 10001th prime
        104743
    """
    primes = [2, 3, 5, 7, 11]

    for p in primes:
        yield p

    n = primes[-1] + 2

    while True:
        sqrt = math.sqrt(n)

        for p in primes:
            if not n % p:
                break
            elif p > sqrt:
                primes.append(n)
                yield n
                break

        # all primes are odd, and as we started with 5...
        n += 2

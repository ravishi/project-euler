import math
import data
import util

def problem1():
    """"Add all the natural numbers below one thousand that are
    multiples of 3 or 5."""
    return sum(n for n in xrange(1000) if not n % 3 or not n % 5)

def problem2():
    from itertools import takewhile
    def fib():
        a = 0;
        b = 1
        while 1:
            c = a + b
            a = b
            b = c
            yield a
    ceil = 4 * 10 ** 6
    return sum(n for n in takewhile(lambda x: x < ceil, fib()) if not n % 2)

def problem3():
    def factorize(natural):
        n = natural
        check = 2
        factors = []
        while check * check <= n:
            if n % check == 0:
                factors.append(check)
                n = n / check
            else:
                check += 1
        if not n == 1:
            factors.append(n)
        return factors

    n = 600851475143
    factors = factorize(n)
    return tuple(sorted(factors))[-1]

def problem4():
    def ispalindromic(n):
        s = str(n)
        return s == s[::-1]
    found = 0, 0
    for a in xrange(999, 0, -1):
        for b in xrange(999, 0, -1):
            if ispalindromic(a * b):
                c, d = found
                if a * b > c * d:
                    found = a, b
    a, b = found
    return a * b

def problem5():
    def lcm(a, b):
        return abs(a * b) / gcd(a, b)

    def gcd(a, b):
        if not b:
            return a
        return gcd(b, a % b)

    rng = xrange(1, 21)
    i = 1
    for n in rng:
        i = lcm(i, n)
    return i

def problem6():
    ceil = 100
    square = lambda x: x ** 2
    rng = range(1, 1+ceil)
    sumosq = sum(map(square, rng))
    sqosum = sum(rng) ** 2
    return sqosum - sumosq

def problem7():
    """Find the 10001st prime."""
    NTH = 10001
    primes = [2, 3, 5, 7]
    n = 11
    while len(primes) < NTH:
        sqrt = math.sqrt(n)

        for p in primes:
            if not n % p:
                break
            elif p > sqrt:
                primes.append(n)
                break
        # all primes are odd
        n += 2
    return primes[-1]

def problem8():
    """Find the greatest product of five consecutive digits in the
    1000-digit number."""
    import operator

    digits = map(int, data.problem8)

    lastfive = []
    result = 0
    for d in digits:
        lastfive.append(d)
        if len(lastfive) > 5:
            lastfive.pop(0)

        s = reduce(operator.mul, lastfive)

        if s > result:
            result = s

    return result

def problem9():
    """Find the only Pythagorean triplet, {a, b, c}, for
    which a + b + c = 1000."""
    for a in range(1, 999):
        for b in range(a + 1, 999 - a - 1):
            c = 1000 - a - b
            if c <= b:
                break
            if a * a + b * b == c * c:
                return a * b * c

def problem10():
    """Find the sum of all the primes below two million."""
    TOP = 2000000

    def primegen():
        """
        A prime generator. One can assert its ok based on the solution of
        problem 07.::

            >>> g = iter(primegen())
            >>> assert [g.next() for i in range(10002)][-1] == 104743
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
                    yield n
                    primes.append(n)
                    break

            # all primes are odd, and as we started with 5...
            n += 2

    g = iter(primegen())
    s = 0
    cur = 0
    while cur <= TOP:
        s += cur
        cur = g.next()
    return s

def problem11():
    """What is the greatest product of four adjacent numbers in any
    direction (up, down, left, right, or diagonally) in the 2020 grid?"""
    # ok, I copied this one. shame on me. but this solution is so pretty!
    import operator
    grid = [map(int, line.split()) for line in data.problem11.strip().splitlines()]
    product = lambda x: reduce(operator.mul, x)
    grid_get = lambda grid, x, y: grid[y][x] if 0 <= y < len(grid) and 0 <= x < len(grid[0]) else 0
    diffs = ((0, 1), (1, 0), (1, 1), (1, -1))
    return max(product(grid_get(grid, x + i * dx, y + i * dy) for i in range(4)) for y in range(len(grid)) for x in range(len(grid[0])) for (dx, dy) in diffs)

def problem13():
    """Work out the first ten digits of the sum of the following
    one-hundred 50-digit numbers."""
    numbers = map(int, data.problem13.strip().splitlines())
    return int(str(sum(numbers))[:10])

def problem16():
    """What is the sum of the digits of the number 21000?"""
    return sum(map(int, str(2 ** 1000)))

def problem36():
    """Find the sum of all numbers less than one million, which are
    palindromic in base 10 and base 2."""
    def palindromic(s):
        return s == s[::-1]
    return sum(n for n in xrange(int(10e5) + 1)
               if palindromic(str(n)) and palindromic(util.itoa(n, 2)))

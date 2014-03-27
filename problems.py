import math
import data
import util


def problem1():
    """"Add all the natural numbers below one thousand that are
    multiples of 3 or 5."""
    def msum(r, ceil):
        ceil -= 1
        last = ceil - ceil%r
        n = last / r
        return (r + last) * n / 2
    return msum(3, 1000) + msum(5, 1000) - msum(15, 1000)


def problem2():
    """By considering the terms in the Fibonacci sequence whose
    values do not exceed four million, find the sum of the
    even-valued terms."""
    from itertools import takewhile
    def fib():
        a, b = 0, 1
        while 1:
            a, b = b, a + b
            yield a
    ceil = 4 * 10 ** 6
    return sum(n for n in takewhile(lambda x: x < ceil, fib()) if not n % 2)


def problem3():
    """Find the largest prime factor of a composite number."""
    def factorize(natural):
        n = natural
        check = 2
        while check * check <= n:
            if n % check == 0:
                yield check
                n = n / check
            else:
                check += 1
        if not n == 1:
            yield n

    n = 600851475143
    return sorted(factorize(n))[-1]


def problem4():
    """Find the largest palindrome made from the product of two 3-digit
    numbers."""
    def ispalindromic(n):
        s = str(n)
        return s == s[::-1]

    found = 0, 0

    for a in range(999, 0, -1):
        for b in range(999, 0, -1):
            if ispalindromic(a * b):
                c, d = found
                if a * b > c * d:
                    found = a, b
    a, b = found
    return a * b


def problem5():
    """What is the smallest number divisible by each of
    the numbers 1 to 20?"""
    from functools import reduce
    return reduce(util.lcm, range(1, 21), 10)


def problem6():
    """What is the difference between the sum of the squares and
    the square of the sums?"""
    ceil = 100
    square = lambda x: x ** 2
    sum_of_squares = sum(map(square, range(1, ceil + 1)))
    square_of_sum = sum(range(1, ceil + 1)) ** 2
    return  square_of_sum - sum_of_squares


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
    from functools import reduce

    digits = map(int, data.problem8)

    result = 0
    lastfive = []

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
    ceil = 1000
    for a in range(1, ceil - 1):
        for b in range(a + 1, ceil - a - 2):
            c = ceil - a - b
            if c <= b:
                break
            if a * a + b * b == c * c:
                return a * b * c


def problem10():
    """Find the sum of all the primes below two million."""
    from itertools import takewhile
    ceil = 2000000
    return sum(n for n in takewhile(lambda x: x < ceil, util.primegen()))


def problem11():
    """What is the greatest product of four adjacent numbers in any
    direction (up, down, left, right, or diagonally) in the 2020 grid?"""
    # ok, I copied this one. shame on me. but this solution is so pretty!
    import operator
    from functools import reduce
    grid = [list(map(int, line.split())) for line in data.problem11.strip().splitlines()]
    product = lambda x: reduce(operator.mul, x)
    grid_get = lambda grid, x, y: grid[y][x] if 0 <= y < len(grid) and 0 <= x < len(grid[0]) else 0
    diffs = ((0, 1), (1, 0), (1, 1), (1, -1))
    return max(product(grid_get(grid, x + i * dx, y + i * dy) for i in range(4)) for y in range(len(grid)) for x in range(len(grid[0])) for (dx, dy) in diffs)


def problem12():
    """What is the value of the first triangle number to have over five
    hundred divisors?"""

    # first thing, trinangle numbers can be calculated by the formula:
    #
    #   t(n) = n * (n + 1) / 2
    #
    # where t(n) is the value of the nth triangle number
    #
    # after that, we use the Sum of Divisors function [1] to compute
    # the number of divisors of a number

    from util import primegen
    from collections import Counter
    from operator import mul
    from functools import reduce

    def trianglenum(nth):
        return nth * (nth + 1) / 2

    # we'll reuse our simple `primegen` function to generate primes. but
    # we want to save the generated primes, since we'll be using them
    # for more than one iteration.
    _primes = []
    _primes_generator = primegen()

    def primes():
        for p in _primes:
            yield p
        for p in _primes_generator:
            _primes.append(p)
            yield p

    # now we go through the triangle numbers, counting their divisors
    i = 1
    while True:
        n = trianglenum(i)
        i += 1

        factors = []

        # break n into prime factors
        r = n
        g = primes()

        while r > 1:
            p = next(g)
            while r > 1 and r % p == 0:
                factors.append(p)
                r /= p

        # count the prime factors of n
        counter = Counter(factors)

        # multiply the count of prime factors accordingly to the sum of
        # divisors formula
        d = reduce(mul, (n + 1 for n in counter.values()), 1)

        if d > 500:
            return n


def problem13():
    """Work out the first ten digits of the sum of the following
    one-hundred 50-digit numbers."""
    numbers = map(int, data.problem13.strip().splitlines())
    return int(str(sum(numbers))[:10])


def problem16():
    """What is the sum of the digits of the number 21000?"""
    return sum(map(int, str(2 ** 1000)))


def problem19():
    """How many Sundays fell on the first of the month during the
    twentieth century (1 Jan 1901 to 31 Dec 2000)?"""
    def isleap(year):
        return year % 4 == 0 and (not year % 100 == 0 or year % 400 == 0)

    def mdays(year, month):
        if month == 2:
            return 28 if not isleap(year) else 29
        elif month in (4, 6, 9, 11):
            return 30
        else:
            return 31

    sundays = 1
    acc_days = 0
    for year in range(1901, 2001):
        for month in range(1, 13):
            acc_days += mdays(year, month)
            if acc_days % 7 == 0:
                sundays += 1

    return sundays


def problem36():
    """Find the sum of all numbers less than one million, which are
    palindromic in base 10 and base 2."""
    def palindromic(s):
        return s == s[::-1]
    return sum(n for n in range(int(10e5) + 1)
               if palindromic(str(n)) and palindromic(util.itoa(n, 2)))

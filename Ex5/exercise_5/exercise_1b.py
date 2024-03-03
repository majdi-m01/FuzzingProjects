"""
Use this file to implement your solution for exercise 5-1 b.
"""

from exercise_1a import *
from fuzzingbook.Coverage import Location

def lcsaj_n(trace: list[Location], n: int) -> set[tuple[Location, ...]]:
    if n <= 0:
        raise ValueError("Parameter n must be greater than 0")

    coverage_elements = list(lcsaj(trace))
    result = set()

    for i in range(len(coverage_elements) - n + 1):
        result.add(tuple(coverage_elements[i:i + n]))

    return result
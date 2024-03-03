"""
Use this file to implement your solution for exercise 5-1 a.
"""
from fuzzingbook.Coverage import Location

def lcsaj(trace: list[Location]) -> set[tuple[Location, ...]]:
    coverage_elements = []
    current_sequence = []

    if trace:
        current_sequence.append(trace[0])

    for current_location, next_location in zip(trace, trace[1:]):
        current_element, current_line = current_location
        next_element, next_line = next_location

        if current_element != next_element or current_line + 1 != next_line:
            coverage_elements.append(tuple(current_sequence + [next_location]))
            current_sequence = [next_location]
        else:
            current_sequence.append(next_location)

    coverage_elements.append(tuple(current_sequence))
    return set(coverage_elements)
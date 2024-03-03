import sys

from fuzzingbook.PythonFuzzer import PythonFuzzer

from exercise_1a import constraint as constraint_1a
from exercise_1b import constraint as constraint_1b
from exercise_1c import constraint as constraint_1c
from exercise_1d import constraint as constraint_1d


def fuzz(constraint: str):
    fuzzer = PythonFuzzer(constraint=constraint)
    return fuzzer.fuzz()

def main():
    assert len(sys.argv) == 2
    subexercise = sys.argv[1]
    assert subexercise in ["1a", "1b", "1c", "1d"], "Invalid subexercise!"

    print(f"Generating a program with the constraint of exercise {subexercise}...")
    if subexercise == "1a":
        p = fuzz(constraint_1a)
    elif subexercise == "1b":
        p = fuzz(constraint_1b)
    elif subexercise == "1c":
        p = fuzz(constraint_1c)
    elif subexercise == "1d":
        p = fuzz(constraint_1d)
    
    print("Solution:")
    print(p)

if __name__ == "__main__":
    main()
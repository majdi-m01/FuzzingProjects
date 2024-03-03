import subprocess
from typing import Tuple, Any

from fuzzingbook.Fuzzer import Outcome

from exercise_1 import levenshtein_distance
from fuzzingbook import Fuzzer


class FunctionRunner(Fuzzer.ProgramRunner):

    def run_process(self, inp: str = ""):
        return self.program(inp)

    def run(self, inp: str = "") -> Tuple[Tuple[str, Any], Outcome]:
        try:
            execution = self.run_process(inp)
            outcome = self.PASS
        except LookupError:
            outcome = self.FAIL
            execution = None
        except:
            outcome = self.UNRESOLVED
            execution = None
        return (inp, execution), outcome


def ld_wrapper(inp):
    segments = inp.split('+')
    if len(segments) < 2:
        raise ValueError
    return levenshtein_distance(segments[0], segments[1])


def run():
    random_fuzzer = Fuzzer.RandomFuzzer(min_length=2, max_length=10, char_start=43, char_range=10)
    return random_fuzzer.runs(runner=FunctionRunner(ld_wrapper), trials=10)


if __name__ == '__main__':
    for result in run():
        print(result)

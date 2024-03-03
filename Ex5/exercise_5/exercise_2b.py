"""
Use this file to implement your solution for exercise 5-1 b.
"""
from fuzzingbook.Fuzzer import RandomFuzzer
from exercise_2a import FunctionCoverageRunner
import html


class RandomCoverageFuzzer(RandomFuzzer):
    
    def runs(self, runner: FunctionCoverageRunner):
      outcomes = []
      total_coverage = set()
      consecutive_runs = 0

      while consecutive_runs < 10:
        outcome = self.run(runner)
        outcomes.append(outcome)

        if runner.coverage.issubset(total_coverage):
            consecutive_runs += 1
        else:
            total_coverage.update(runner.coverage)
            consecutive_runs = 0

      return outcomes


if __name__ == '__main__':
    fuzzer = RandomCoverageFuzzer()
    print(fuzzer.runs(FunctionCoverageRunner(html.escape)))
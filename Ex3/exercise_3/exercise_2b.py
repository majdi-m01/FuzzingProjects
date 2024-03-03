"""
Use this file to implement your solution for exercise 3-2 a.
"""

from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
from re_coverage import get_coverage

from exercise_2 import RE_GRAMMAR
from exercise_2a import RE_GRAMMAR_EXPANDED

import random

random.seed()


def average_coverage(fuzzer, grammar, num_trials=25):
    total_coverage = sum(get_coverage(fuzzer(grammar)) for _ in range(num_trials))
    return total_coverage / num_trials


# run the experiment for GrammarFuzzer with RE_GRAMMAR
GrammarFuzzerREGrammar = average_coverage(GrammarFuzzer, RE_GRAMMAR)
# run the experiment for GrammarCoverageFuzzer with RE_GRAMMAR
GrammarCoverageFuzzerREGrammar = average_coverage(GrammarCoverageFuzzer, RE_GRAMMAR)
# run the experiment for GrammarCoverageFuzzer with RE_GRAMMAR_EXPANDED
GrammarCoverageFuzzerREGrammarExpanded = average_coverage(GrammarCoverageFuzzer, RE_GRAMMAR_EXPANDED)

print('GrammarFuzzer: {}'.format(
    GrammarFuzzerREGrammar))  # print the average code coverage for GrammarFuzzer + RE_GRAMMAR
print('GrammarCoverageFuzzer: {}'.format(
    GrammarCoverageFuzzerREGrammar))  # print the average code coverage for GrammarCoverageFuzzer + RE_GRAMMAR
print('GrammarCoverageFuzzer+: {}'.format(
    GrammarCoverageFuzzerREGrammarExpanded))  # print the average code coverage for GrammarCoverageFuzzer + RE_GRAMMAR_EXPANDED

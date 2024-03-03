from fuzzingbook import Coverage

import re

def get_coverage(fuzzer):
    overall_cov = set()
    for _ in range(5):
        s = fuzzer.fuzz()
        with Coverage.Coverage() as cov:
            re.compile(s)
        overall_cov |= cov.coverage()
    return len(overall_cov)

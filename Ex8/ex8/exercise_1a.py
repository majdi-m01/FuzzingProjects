from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer
from fuzzingbook.GreyboxFuzzer import GreyboxFuzzer, PowerSchedule, Mutator
from fuzzingbook.GreyboxGrammarFuzzer import LangFuzzer, GreyboxGrammarFuzzer, FragmentMutator, AFLSmartSchedule, RegionMutator
from fuzzingbook.Parser import EarleyParser


def get_random_fuzzer() -> RandomFuzzer:
    return RandomFuzzer()


def get_grammar_fuzzer(grammar) -> GrammarFuzzer:
    return GrammarFuzzer(grammar)


def get_mutation_fuzzer(seeds) -> MutationFuzzer:
    return MutationFuzzer(seed=seeds)


def get_greybox_fuzzer(seeds) -> GreyboxFuzzer:
    mutator = Mutator()
    powerSchedule = PowerSchedule()
    return GreyboxFuzzer(seeds=seeds, mutator=mutator, schedule=powerSchedule)


def get_lang_fuzzer(seeds, grammar) -> LangFuzzer:
    earleyParser = EarleyParser(grammar)
    fragmentMutator = FragmentMutator(earleyParser)
    powerSchedule = PowerSchedule()
    return LangFuzzer(seeds, fragmentMutator, powerSchedule)


def get_greybox_grammar_fuzzer(seeds, grammar) -> GreyboxGrammarFuzzer:
    earleyParser = EarleyParser(grammar)
    aflSmartSchedule = AFLSmartSchedule(earleyParser)
    regionMutator = RegionMutator(earleyParser)
    mutator = Mutator()
    return GreyboxGrammarFuzzer(seeds, mutator, regionMutator, aflSmartSchedule)

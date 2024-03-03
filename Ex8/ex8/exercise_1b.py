import time
import os

from fuzzingbook.MutationFuzzer import FunctionRunner, FunctionCoverageRunner
from fuzzingbook.Coverage import population_coverage

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#from html_grammar import HTML_GRAMMAR
import string
from fuzzingbook.Grammars import srange, is_valid_grammar

HTML_GRAMMAR = {
    '<start>': ['<doctype><html>'],
    '<doctype>': ['<lt>!DOCTYPE html<gt>', # html5
                  '<lt>!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"<gt>', # html4
                  '<lt>!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"<gt>', # html3
                 ],
    '<html>': ['<head><body>'],
    '<head>': ['<lt>head<gt><header_content><lt>/head<gt>'],
    '<body>': ['<lt>body<gt><body_content><lt>/body<gt>'],
    '<header_content>': ['',
                         '<title><header_content>',
                         '<meta><header_content>'],
    '<title>': ['<lt>title<gt><title_content><lt>/title<gt>'],
    '<title_content>': ['', '<title_char><title_content>'],
    '<title_char>': srange(string.ascii_letters + string.digits + "',-_ "),
    '<meta>': ['<lt>meta <meta_attributes><gt>'],
    '<meta_attributes>': ['charset="UTF-8"',  'name="author" content="<author>"'],
    '<author>': ['<chars>'],
    '<body_content>': ['',
                       '<div><body_content>', 
                       '<p><body_content>', 
                       '<ul><body_content>', 
                       '<ol><body_content>', 
                       '<text><body_content>'],
    '<div>': ['<lt>div<gt><body_content><lt>/div<gt>'],
    '<p>': ['<lt>p<gt><text><lt>/p<gt>'],
    '<ul>': ['<lt>ul<gt><list><lt>/ul<gt>'],
    '<ol>': ['<lt>ol<gt><list><lt>/ol<gt>'],
    '<list>': ['', '<lt>li<gt><body_content><lt>/li<gt><list>'],
    '<lt>': ['<'],
    '<gt>': ['>'],
    '<br>': ['<lt>br<gt>'],
    '<text>': ['', '<chars><br><text>'],
    '<chars>': ['', '<char><chars>'],
    '<char>': srange(string.printable),
}

assert is_valid_grammar(HTML_GRAMMAR)


#from exercise_1a import *
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

##############

def get_runner():
    return FunctionRunner(parse_html)


def get_coverage_runner():
    return FunctionCoverageRunner(parse_html)


def parse_html(html):
    return BeautifulSoup(html, features="lxml")


if __name__ == '__main__':
    trials = 1000
    
    seeds = []
    for i in range(50):
        with open(os.path.join('html', f'{i}.html'), 'r') as fp:
            seeds.append(fp.read())
    
    #####
    random_fuzzer = get_random_fuzzer()
    runner = get_runner()

    random_fuzzer_inputs = []
    start = time.time()
    for _ in range(trials):
        random_fuzzer_inputs.append(random_fuzzer.fuzz())
    end = time.time()

    print("It took the random fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    grammar_fuzzer = get_grammar_fuzzer(HTML_GRAMMAR)
    runner = get_runner()

    grammar_fuzzer_inputs = []
    start = time.time()
    for _ in range(trials):
        grammar_fuzzer_inputs.append(grammar_fuzzer.fuzz())
    end = time.time()

    print("It took the grammar fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    mutation_fuzzer = get_mutation_fuzzer(seeds)
    runner = get_runner()

    mutation_fuzzer_inputs = []
    start = time.time()
    for _ in range(trials):
        mutation_fuzzer_inputs.append(mutation_fuzzer.fuzz())
    end = time.time()

    print("It took the mutation fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    greybox_fuzzer = get_greybox_fuzzer(seeds)
    runner = get_coverage_runner()

    start = time.time()
    greybox_fuzzer.runs(runner, trials=trials)
    end = time.time()

    print("It took the greybox fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    lang_fuzzer = get_lang_fuzzer(seeds, HTML_GRAMMAR)
    runner = get_coverage_runner()

    start = time.time()
    lang_fuzzer.runs(runner, trials=trials)
    end = time.time()

    print("It took the lang fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    greybox_grammar_fuzzer = get_greybox_grammar_fuzzer(seeds, HTML_GRAMMAR)
    runner = get_coverage_runner()

    start = time.time()
    greybox_grammar_fuzzer.runs(runner, trials=trials)
    end = time.time()

    print("It took the greybox grammar fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    _, random_cov = population_coverage(random_fuzzer_inputs, parse_html)
    _, grammar_cov = population_coverage(grammar_fuzzer_inputs, parse_html)
    _, mutation_cov = population_coverage(mutation_fuzzer_inputs, parse_html)
    _, greybox_cov = population_coverage(greybox_fuzzer.inputs, parse_html)
    _, lang_cov = population_coverage(lang_fuzzer.inputs, parse_html)
    _, greybox_grammar_cov = population_coverage(greybox_grammar_fuzzer.inputs, parse_html)

    line_random, = plt.plot(random_cov, label="Random")
    line_grammar, = plt.plot(grammar_cov, label="Grammar")
    line_mutation, = plt.plot(mutation_cov, label="Mutaion")
    line_greybox, = plt.plot(greybox_cov, label="Greybox")
    line_lang, = plt.plot(lang_cov, label="Lang")
    line_greybox_grammar, = plt.plot(greybox_grammar_cov, label="GreyboxGrammar")
    plt.legend(handles=[line_random, line_grammar, line_mutation, line_greybox, line_lang, line_greybox_grammar])
    plt.xlim(0, trials)
    plt.title('Coverage over time')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');
    plt.savefig('plots.png')
    
    with open('results_1b.py', 'w') as fp:
        fp.write(f'random_cov = {random_cov}\n')
        fp.write(f'grammar_cov = {grammar_cov}\n')
        fp.write(f'mutation_cov = {mutation_cov}\n')
        fp.write(f'greybox_cov = {greybox_cov}\n')
        fp.write(f'lang_cov = {lang_cov}\n')
        fp.write(f'greybox_grammar_cov = {greybox_grammar_cov}\n')

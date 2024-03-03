"""
Use this file to evaluate your solution. Please do not modify.
"""

import random
import json
import argparse

from fuzzingbook.Parser import EarleyParser

from printer_grammar import PRINTER_GRAMMAR
from helpers import read_inputs, tree_to_string
from implementation import instantiate_with_nonterminals, instantiate_with_subtrees, check, learn, generate
from oracles import has_warranty_xor_needs_check, manufacturer_in_model_with_check_must_be_zero, serial_in_model_and_check_not_in_model, status_length_equals_copies_printed, type_length_xor_copies_printed_equals_one, type_length_xor_status_length_equals_zero
from tests import test_instantiate_with_nonterminals, test_instantiate_with_subtrees, test_check, test_learn, test_generate

constraint_patterns = [
    "int(str({})) == 0",
    "int(str({})) == 1",
    "int(str({})) != 0",
    "int(str({})) != 1",
    "int(str({})) >= 0",
    "int(str({})) >= 1",

    "str({}) == str({})",
    "str({}) in str({})",
    "str({}) not in str({})",

    "len(str({})) == 0",
    "len(str({})) == 1",
    "len(str({})) == int({})",
    "len(str({})) == len(str({}))",
    "len(str({})) < len(str({}))",
    "len(str({})) ^ len(str({})) == 0",
    "len(str({})) ^ len(str({})) == 1",
    "len(str({})) ^ int({}) == 0",
    "len(str({})) ^ int({}) == 1",

    "bool(int({})) ^ bool(int({}))"
]

parser = EarleyParser(PRINTER_GRAMMAR)


def run_learn(oracle_name, additional_positive_samples=[], additional_negative_samples=[]):
    print("-------------------------")
    print(oracle_name)

    pos_path = f'inputs/{oracle_name}/passing_inputs.txt'
    neg_path = f'inputs/{oracle_name}/failing_inputs.txt'

    pos_inputs, pos_trees = read_inputs(pos_path, parser)
    neg_inputs, neg_trees = read_inputs(neg_path, parser)

    additional_pos_trees = [next(parser.parse(inp))
                            for inp in additional_positive_samples]
    additional_neg_trees = [next(parser.parse(inp))
                            for inp in additional_negative_samples]

    pos_trees = pos_trees + additional_pos_trees
    neg_trees = neg_trees + additional_neg_trees

    pos_constraints: set = learn(constraint_patterns, pos_trees)
    neg_constraints: set = learn(constraint_patterns, neg_trees)
    diff = pos_constraints.difference(neg_constraints)

    print(" Learned constraint set:")
    print(diff)
    print("-------------------------")
    return diff


def validate_constraint(constraints: set[str], grammar: dict, oracle: callable) -> tuple[list, list]:
    new_pos_samples = []
    new_neg_samples = []

    for i in range(100):
        inp = generate(constraints, grammar, produce_valid_sample=True)
        printer_json = json.loads(inp)
        if not oracle(printer_json):
            new_pos_samples.append(inp)
    for i in range(100):
        inp = generate(constraints, grammar, produce_valid_sample=False)
        printer_json = json.loads(inp)
        if oracle(printer_json):
            new_neg_samples.append(inp)

    # return [], [] means: constraint is validated.
    return new_pos_samples, new_neg_samples


def learn_and_refine(oracle_name, grammar, oracle):
    constraints: set = run_learn(oracle_name)
    additional_positive_samples, additional_negative_samples = validate_constraint(
        constraints, grammar, oracle)

    limit = 10
    tries = 0
    while additional_positive_samples != [] or additional_negative_samples != []:
        tries += 1
        if tries == limit:
            print("learn_and_refine failed.")
            return None
        constraints: set = run_learn(
            oracle_name, additional_positive_samples, additional_negative_samples)
        additional_positive_samples, additional_negative_samples = validate_constraint(
            constraints, grammar, oracle)

    print("learn_and_refine successful.")
    return constraints


def main():
    random.seed()

    parser = argparse.ArgumentParser(description='Project 2')

    test_group = parser.add_argument_group(
        'Test Options', 'Options for enabling tests.')
    test_group.add_argument('--test-instantiate-nonterminals', action='store_true',
                            help='Do test test_instantiate_with_nonterminals.')
    test_group.add_argument('--test-instantiate-subtrees', action='store_true',
                            help='Do test test_instantiate_with_subtrees.')
    test_group.add_argument(
        '--test-check', action='store_true', help='Do test check.')
    test_group.add_argument(
        '--test-learn', action='store_true', help='Do test learn.')
    test_group.add_argument(
        '--test-generate', action='store_true', help='Do test generate.')
    test_group.add_argument(
        '--test-all', action='store_true', help='Do all tests.')

    main_options = parser.add_argument_group(
        'Main Options', 'Options for the project.')
    main_options.add_argument(
        "--learn-oracle-1", action='store_true', help='Learn the constraints of oracle 1.')
    main_options.add_argument(
        "--learn-oracle-2", action='store_true', help='Learn the constraints of oracle 2.')
    main_options.add_argument(
        "--learn-oracle-3", action='store_true', help='Learn the constraints of oracle 3.')
    main_options.add_argument(
        "--learn-oracle-4", action='store_true', help='Learn the constraints of oracle 4.')
    main_options.add_argument(
        "--learn-oracle-5", action='store_true', help='Learn the constraints of oracle 5.')
    main_options.add_argument(
        "--learn-oracle-6", action='store_true', help='Learn the constraints of oracle 6.')
    main_options.add_argument(
        "--learn-all", action='store_true', help='Learn the constraints of all oracles.')

    args = parser.parse_args()

    # <TESTS>
    if args.test_all:
        args.test_instantiate_nonterminals = True
        args.test_instantiate_subtrees = True
        args.test_check = True
        args.test_learn = True
        args.test_generate = True

    if args.test_instantiate_nonterminals:
        test_instantiate_with_nonterminals()
    if args.test_instantiate_subtrees:
        test_instantiate_with_subtrees()
    if args.test_check:
        test_check()
    if args.test_learn:
        test_learn()
    if args.test_generate:
        test_generate()
    # </TESTS>

    # <MAIN>
    if args.learn_all:
        args.learn_oracle_1 = True
        args.learn_oracle_2 = True
        args.learn_oracle_3 = True
        args.learn_oracle_4 = True
        args.learn_oracle_5 = True
        args.learn_oracle_6 = True

    import time

    start_time = time.time()

    if args.learn_oracle_1:
        learn_and_refine("has_warranty_xor_needs_check",
                         PRINTER_GRAMMAR, has_warranty_xor_needs_check)

    if args.learn_oracle_2:
        learn_and_refine("manufacturer_in_model_with_check_must_be_zero",
                         PRINTER_GRAMMAR, manufacturer_in_model_with_check_must_be_zero)

    if args.learn_oracle_3:
        learn_and_refine("serial_in_model_and_check_not_in_model",
                         PRINTER_GRAMMAR, serial_in_model_and_check_not_in_model)

    if args.learn_oracle_4:
        learn_and_refine("status_length_equals_copies_printed",
                         PRINTER_GRAMMAR, status_length_equals_copies_printed)

    if args.learn_oracle_5:
        learn_and_refine("type_length_xor_copies_printed_equals_one",
                         PRINTER_GRAMMAR, type_length_xor_copies_printed_equals_one)

    if args.learn_oracle_6:
        learn_and_refine("type_length_xor_status_length_equals_zero",
                         PRINTER_GRAMMAR, type_length_xor_status_length_equals_zero)

    # print total time taken  in seconds
    print("--- %s seconds ---" % (time.time() - start_time))

    print("done.")


if __name__ == "__main__":
    main()

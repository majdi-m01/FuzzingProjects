"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.Parser import EarleyParser

from helpers import is_nt, tree_to_string, get_all_subtrees


def instantiate_with_nonterminals(constraint_pattern: str, nonterminals: list[str]) -> set[str]:
    instantiated_constraints = set()
    placeholders_count = constraint_pattern.count("{}")

    if placeholders_count == 1:
        for nt in nonterminals:
            # Ensure the symbol is a non-terminal before instantiation
            if is_nt(nt):
                instantiated_constraints.add(constraint_pattern.format(nt))
    elif placeholders_count == 2:
        for nt1 in nonterminals:
            for nt2 in nonterminals:
                # Ensure both symbols are non-terminals before instantiation
                if is_nt(nt1) and is_nt(nt2):
                    instantiated_constraints.add(constraint_pattern.format(nt1, nt2))
    return instantiated_constraints


def instantiate_with_subtrees(abstract_constraint: str, nts_to_subtrees: dict) -> set[str]:

    # Helper function to replace non-terminal in the constraint with its subtree representations
    def replace_nt_with_subtrees(abstract_constraint, nt, subtrees):
        return [abstract_constraint.replace(nt, tree_to_string(subtree)) for subtree in subtrees]

    concrete_constraints = set([abstract_constraint])  # Initialize with the abstract constraint

    for nt, subtrees in nts_to_subtrees.items():
        new_constraints = set()
        for constraint in concrete_constraints:
            if nt in constraint:
                # Replace current non-terminal with each of its subtree representations
                instantiated = replace_nt_with_subtrees(constraint, nt, subtrees)
                new_constraints.update(instantiated)
            else:
                # If the non-terminal is not in the current constraint, just carry it over
                new_constraints.add(constraint)
        concrete_constraints = new_constraints

    return concrete_constraints

import itertools

def learn(constraint_patterns: list[str], derivation_trees: list) -> set[str]:
    # Extract common nonterminal symbols from all derivation trees
    common_nonterminals = get_common_nonterminals(derivation_trees)

    # Instantiate the constraint patterns with these nonterminal symbols
    instantiated_constraints = set()
    for pattern in constraint_patterns:
        for combo in itertools.product(common_nonterminals, repeat=pattern.count("{}")):
            instantiated_constraint = pattern.format(*combo)
            if all(check_constraint(instantiated_constraint, tree) for tree in derivation_trees):
                instantiated_constraints.add(instantiated_constraint)

    return instantiated_constraints

def get_common_nonterminals(derivation_trees):
    all_nts_sets = []
    for tree in derivation_trees:
        nts_to_subtrees = get_all_subtrees(tree)
        all_nts_sets.append(set(nts_to_subtrees.keys()))

    # Find common nonterminal symbols across all trees
    common_nts = set.intersection(*all_nts_sets) if all_nts_sets else set()
    return common_nts

def check_constraint(constraint, tree):
    nts_to_subtrees = get_all_subtrees(tree)
    concrete_constraints = instantiate_with_subtrees(constraint, nts_to_subtrees)
    for concrete_constraint in concrete_constraints:
        try:
            if not eval(concrete_constraint):
                return False  # Break early if a constraint does not hold
        except Exception as e:
            return False  # Assuming failure on exception
    return True

def check(abstract_constraints: set[str], derivation_tree) -> bool:
    # Extract subtrees rooted at non-terminal symbols from the derivation tree
    nts_to_subtrees = get_all_subtrees(derivation_tree)

    for abstract_constraint in abstract_constraints:
        concrete_constraints = instantiate_with_subtrees(abstract_constraint, nts_to_subtrees)

        # If no concrete constraints are generated, then the abstract constraint cannot hold
        if not concrete_constraints:
            return False

        # Check if at least one concrete constraint holds true
        for constraint in concrete_constraints:
            try:
                if not any([eval(constraint)]):
                    # Return False if the abstract constraint does not hold for any subtree
                    return False
            except ValueError as e:
                continue
            except TypeError as e:
                continue
            except SyntaxError as e:
                continue
    # If all abstract constraints have at least one concrete constraint that holds, return True
    return True


def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: bool) -> str:
    fuzzer = GrammarFuzzer(grammar)
    while True:
        inp = fuzzer.fuzz()
        parser = EarleyParser(grammar)
        try:
            tree = next(parser.parse(inp))
            if check(abstract_constraints, tree) == produce_valid_sample:
                return inp
        except StopIteration:
            continue  # If parsing fails, try again
    return None


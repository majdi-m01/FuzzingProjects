"""
Utilities for parsing and processing tree structures.
"""

from fuzzingbook.Parser import EarleyParser


def is_nt(symbol):
    """
    Checks if a given symbol is a non-terminal symbol..

    Args:
        symbol (str): The symbol to check.

    Returns:
        bool: True if the symbol is a non-terminal symbol, False otherwise.
    """
    return symbol and (symbol[0], symbol[-1]) == ('<', '>')


def get_all_subtrees(tree, subtrees=None) -> dict:
    """
    Traverses a given parse tree and extracts all subtrees.

    Args:
        tree (tuple)
        subtrees (dict): A dictionary to store the subtrees. Should be None initially.

    Returns:
        dict: A dictionary mapping non-terminal symbols to a list of subtrees rooted at the non-terminal symbol of the dictionary key.
    """
    if subtrees == None:
        subtrees = dict()

    node, children = tree
    if children != []:
        assert is_nt(node)
        if node not in subtrees:
            subtrees[node] = []
        subtrees[node].append(tree)
        for child in children:
            get_all_subtrees(child, subtrees)

    return subtrees


def tree_to_string(tree, wrap=lambda ntree, depth, name, string: string, depth=0):
    """
    Convert a tree into a string representation.

    Args:
        tree (tuple): The tree to be converted.
        wrap (function, optional): Pass None here.
        depth (int, optional): Leave as-is.

    Returns:
        str: The string representation of the tree.
    """
    name, children, *rest = tree
    if not is_nt(name):
        return name
    else:
        return wrap(tree, depth, name, ''.join([tree_to_string(c, wrap, depth-1) for c in children]))


def read_inputs(path, p: EarleyParser):
    """
    Read inputs from a file and parse them using an EarleyParser instance.

    Args:
        path (str): The path to the file containing the inputs.
        p (EarleyParser): An instance of the EarleyParser class used for parsing.

    Returns:
        tuple: A tuple containing two lists. The first list contains the inputs read from the file,
               and the second list contains the parsed trees corresponding to each input.
    """
    with open(path, "r") as f:
        inputs = f.readlines()
        inputs = [inp.strip() for inp in inputs]
        trees = []
        for inp in inputs:
            tree = next(p.parse(inp))
            trees.append(tree)

    return inputs, trees

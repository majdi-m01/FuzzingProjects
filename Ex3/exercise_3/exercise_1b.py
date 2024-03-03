"""
Use this file to implement your solution for exercise 3-1 b.
"""

import random

from exercise_1a import find_subtrees


def replace_random_subtree(tree, symbol, subtrees):
    possible_subtrees = find_subtrees(tree, symbol)

    if not possible_subtrees:
        return tree

    selected_subtree = random.choice(possible_subtrees)
    replacement_subtree = random.choice(subtrees)

    new_tree = replace_subtree(tree, selected_subtree, replacement_subtree)

    return new_tree


def replace_subtree(tree, target_subtree, replacement_subtree):
    if tree == target_subtree:
        return replacement_subtree

    if isinstance(tree, tuple) and len(tree) == 2:
        nonterminal, children = tree
        if children is not None:
            new_children = [replace_subtree(child, target_subtree, replacement_subtree) for child in children]
        else:
            new_children = None
        return nonterminal, new_children

    return tree

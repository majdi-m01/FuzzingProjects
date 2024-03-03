"""
Use this file to implement your solution for exercise 3-1 a.
"""


def find_subtrees(tree, symbol):
    def recursive_search(node):
        if isinstance(node, tuple) and len(node) == 2:
            nonterminal, children = node

            if nonterminal == symbol:
                subtrees.append(node)

            if children is not None:
                for child in children:
                    recursive_search(child)
    subtrees = []
    recursive_search(tree)
    return subtrees


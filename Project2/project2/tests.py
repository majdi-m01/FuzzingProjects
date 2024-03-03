"""
You can use this file to test your solution. Call each method using arguments in main.py
"""

from fuzzingbook.Parser import EarleyParser
from helpers import tree_to_string
from implementation import instantiate_with_nonterminals, instantiate_with_subtrees, learn, check, generate


def test_instantiate_with_nonterminals():
    # unary
    assert instantiate_with_nonterminals("int({}) == 0", ["<A>", "<B>", "<C>"]) == set(
        ["int(<A>) == 0", "int(<B>) == 0", "int(<C>) == 0"]), "test_instantiate_with_nonterminals failed."
    # binary
    assert instantiate_with_nonterminals("int({}) < {}", ["<A>", "<B>", "<C>"]) == set(["int(<A>) < <A>", "int(<A>) < <B>", "int(<A>) < <C>", "int(<B>) < <A>",
                                                                                        "int(<B>) < <B>", "int(<B>) < <C>",  "int(<C>) < <A>", "int(<C>) < <B>",  "int(<C>) < <C>"]), "test_instantiate_with_nonterminals failed."
    print("test_instantiate_with_nonterminals passed.")


def test_instantiate_with_subtrees():
    Atree1 = ("<A>", [("atree1", [])])
    Atree2 = ("<A>", [("atree2", [])])
    Atree3 = ("<A>", [("atree3", [])])
    Btree1 = ("<B>", [("btree1", [])])
    Btree2 = ("<B>", [("btree2", [])])
    Btree3 = ("<B>", [("btree3", [])])

    # unary
    assert instantiate_with_subtrees("int(<A>) > 0", {"<A>": [Atree1, Atree2, Atree3]}) == set(
        ['int(atree1) > 0', 'int(atree2) > 0', 'int(atree3) > 0']), "test_instantiate_with_subtrees failed."
    # binary
    assert instantiate_with_subtrees("int(<A>) > int(<B>)", {"<A>": [Atree1, Atree2, Atree3], "<B>": [Btree1, Btree2, Btree3], }) == set(['int(atree1) > int(btree1)', 'int(atree1) > int(btree2)', 'int(atree1) > int(btree3)',
                                                                                                                                          'int(atree2) > int(btree1)', 'int(atree2) > int(btree2)', 'int(atree2) > int(btree3)', 'int(atree3) > int(btree1)', 'int(atree3) > int(btree2)', 'int(atree3) > int(btree3)']), "test_instantiate_with_subtrees failed."
    print("test_instantiate_with_subtrees passed.")


def test_check():
    pos_tree1 = ("<A>", [("<value>", [("1000", [])]),
                 ("<price>", [("1", [])])])
    pos_tree2 = ("<A>", [("<value>", [("2000", [])]),
                 ("<price>", [("1", [])])])
    pos_tree3 = ("<A>", [("<value>", [("3000", [])]),
                 ("<price>", [("1", [])])])
    pos_trees = [pos_tree1, pos_tree2, pos_tree3]

    neg_tree1 = ("<A>", [("<value>", [("999", [])]), ("<price>", [("3", [])])])
    neg_tree2 = ("<A>", [("<value>", [("0", [])]), ("<price>", [("2", [])])])
    neg_tree3 = ("<A>", [("<value>", [("-1200", [])]),
                 ("<price>", [("1", [])])])
    neg_tree4 = ("<A>", [("<value>", [("2000", [])]),
                 ("<price>", [("2", [])])])
    neg_tree5 = ("<A>", [("<value>", [("20000", [])]),
                 ("<price>", [("1", [])])])
    neg_trees = [neg_tree1, neg_tree2, neg_tree3, neg_tree4, neg_tree5]

    constraints = set(
        ["int(<price>) == 1", "int(<value>) >= 1000", "len(str(<value>)) == 4"])
    for pos_tree in pos_trees:
        assert check(constraints, pos_tree), "test_check failed."
    for neg_tree in neg_trees:
        assert not check(constraints, neg_tree), "test_check failed."

    print("test_check passed.")


def test_learn():
    pos_tree1 = ("<A>", [("<value>", [("1000", [])]),
                 ("<price>", [("1", [])])])
    pos_tree2 = ("<A>", [("<value>", [("2000", [])]),
                 ("<price>", [("1", [])])])
    pos_tree3 = ("<A>", [("<value>", [("3000", [])]),
                 ("<price>", [("1", [])])])
    pos_trees = [pos_tree1, pos_tree2, pos_tree3]

    neg_tree1 = ("<A>", [("<value>", [("999", [])]), ("<price>", [("3", [])])])
    neg_tree2 = ("<A>", [("<value>", [("1", [])]), ("<price>", [("2", [])])])
    neg_tree3 = ("<A>", [("<value>", [("-2000", [])]),
                 ("<price>", [("1", [])])])
    neg_tree4 = ("<A>", [("<value>", [("2000", [])]),
                 ("<price>", [("2", [])])])
    neg_tree5 = ("<A>", [("<value>", [("20000", [])]),
                 ("<price>", [("1", [])])])
    neg_trees = [neg_tree1, neg_tree2, neg_tree3, neg_tree4, neg_tree5]

    test_patterns = [
        "int(str({})) >= 1000",
        "int(str({})) > 0",
        "str({}) not in str({})",
        "str({}) in str({})",
        "len(str({})) == int({})",
        "len(str({})) == len(str({}))",
        "str({}) == str({})",
        "int(str({})) == 1",
    ]

    pos_constraints: set = learn(test_patterns, pos_trees)
    neg_constraints: set = learn(test_patterns, neg_trees)
    diff = pos_constraints.difference(neg_constraints)

    solution_pos_constraints = set(['str(<price>) in str(<A>)', 'len(str(<value>)) == len(str(<value>))', 'int(str(<price>)) == 1', 'len(str(<price>)) == len(str(<price>))', 'int(str(<A>)) > 0', 'int(str(<value>)) >= 1000', 'str(<A>) not in str(<price>)', 'int(str(<A>)) >= 1000', 'str(<A>) in str(<A>)', 'int(str(<price>)) > 0',
                                   'str(<A>) not in str(<value>)', 'str(<price>) in str(<price>)', 'str(<value>) in str(<value>)', 'str(<A>) == str(<A>)', 'str(<value>) not in str(<price>)', 'str(<value>) in str(<A>)', 'len(str(<price>)) == int(<price>)', 'len(str(<A>)) == len(str(<A>))', 'int(str(<value>)) > 0', 'str(<value>) == str(<value>)', 'str(<price>) == str(<price>)'])
    solution_neg_constraints = set(['len(str(<A>)) == len(str(<A>))', 'str(<price>) in str(<A>)', 'int(str(<price>)) > 0', 'len(str(<price>)) == len(str(<price>))', 'len(str(<value>)) == len(str(<value>))', 'str(<price>) == str(<price>)', 'str(<A>) not in str(<value>)',
                                   'str(<price>) in str(<price>)', 'str(<value>) == str(<value>)', 'str(<value>) in str(<value>)', 'str(<A>) == str(<A>)', 'str(<value>) not in str(<price>)', 'str(<value>) in str(<A>)', 'str(<A>) not in str(<price>)', 'str(<A>) in str(<A>)'])
    solution_diff = set(['int(str(<value>)) > 0', 'int(str(<A>)) > 0', 'int(str(<value>)) >= 1000',
                        'int(str(<price>)) == 1', 'int(str(<A>)) >= 1000', 'len(str(<price>)) == int(<price>)'])

    assert pos_constraints == solution_pos_constraints, "test_learn failed."
    assert neg_constraints == solution_neg_constraints, "test_learn failed."
    assert diff == solution_diff, "test_learn failed."

    print("test_learn passed.")


def test_generate():
    grammar = {"<start>": ["<test>"],
               "<test>": ["First price: <price1>  Second price: <price2> Third price: <price3>"],
               "<price1>": ["<price>"],
               "<price2>": ["<price>"],
               "<price3>": ["<price>"],
               "<price>": ["<leaddigit>", "<leaddigit><digits>"],
               "<leaddigit>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
               "<digits>": ["<digit>", "<digit><digits>"],
               "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]}
    inputs = set()
    while len(inputs) < 10:
        constraints = set(["<price1> > <price2>", "<price2> > <price3>"])
        inp = generate(constraints, grammar, produce_valid_sample=True)
        inputs.add(inp)

    p = EarleyParser(grammar)
    for inp in inputs:
        t = next(p.parse(inp))
        price1 = int(tree_to_string(t[1][0][1][1]))
        price2 = int(tree_to_string(t[1][0][1][3]))
        price3 = int(tree_to_string(t[1][0][1][5]))
        assert price1 > price2 and price2 > price3, "test_generate failed."

    print("test_generated passed.")

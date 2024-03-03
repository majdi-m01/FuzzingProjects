from exercise_1a import find_subtrees
from exercise_1b import replace_random_subtree
from fuzzingbook import Fuzzer
from fuzzingbook import GrammarFuzzer
from fuzzingbook import Grammars
import queue
import random

import trees

class TreeReplaceFuzzer(Fuzzer.Fuzzer):
    
    def __init__(self, grammar, seeds):
        super().__init__()
        self.seeds = seeds
        self.subtrees = dict()
        for rule in grammar:
            self.subtrees[rule] = sum([find_subtrees(s, rule) for s in seeds], start=[])
    
    @staticmethod
    def __find_all_nonterminals__(tree):
        nonterminals = set()
        nodes = queue.Queue()
        nodes.put(tree)
        while not nodes.empty():
            nonterminal, children = nodes.get()
            if children:
                nonterminals.add(nonterminal)
                for child in children:
                    nodes.put(child)
        return list(nonterminals)
    
    def fuzz(self):
        tree = random.choice(self.seeds)
        nonterminal = random.choice(self.__find_all_nonterminals__(tree))
        fuzzed_tree = replace_random_subtree(tree, nonterminal, self.subtrees[nonterminal])
        self.seeds.append(fuzzed_tree)
        return GrammarFuzzer.all_terminals(fuzzed_tree)
    

if __name__ == '__main__':
    fuzzer = TreeReplaceFuzzer(Grammars.EXPR_GRAMMAR, [trees.tree, trees.expr_tree_1, trees.expr_tree_2])
    for _ in range(50):
        print(fuzzer.fuzz())
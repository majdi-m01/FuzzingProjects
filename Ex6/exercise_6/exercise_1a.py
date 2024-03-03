"""
Use this file to implement your solution for exercise 6-1 a.
"""
from inputs import INPS
from parser import parse
from fuzzingbook.GrammarMiner import recover_grammar


def mine_student_grammar() -> dict:
    return recover_grammar(parse, INPS)

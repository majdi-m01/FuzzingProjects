"""
Use this file to implement your solution for exercise 4-1 a.
"""
from fuzzingbook.Grammars import opts

SNAKE_GRAMMAR = {
    '<start>': ['<snake>', ('', opts(prob=0))],
    '<snake>': ['<digit>', ('<snake><digit>', opts(prob=0.6)), ('', opts(prob=0))],
    '<digit>': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
}
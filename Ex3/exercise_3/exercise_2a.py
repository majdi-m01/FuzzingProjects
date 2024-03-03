"""
Use this file to implement your solution for exercise 3-2 a.
"""

RE_GRAMMAR_EXPANDED = {
    '<start>': ['<alternative0>', '^<alternative1>', '<alternative2>$', '^<alternative3>$'],
    '<alternative>': ['<concat>', '<concat>|<alternative>'],
    '<alternative0>': ['<concat>', '<concat>|<alternative0>'],
    '<alternative1>': ['<concat>', '<concat>|<alternative1>'],
    '<alternative2>': ['<concat>', '<concat>|<alternative2>'],
    '<alternative3>': ['<concat>', '<concat>|<alternative3>'],
    '<concat>': ['', '<concat><regex>'],
    '<regex>': ['<symbol0>', '<symbol1>*', '<symbol2>+', '<symbol3>?', '<symbol4>{<range>}'],
    '<symbol0>': ['.', '<char>', '(<alternative>)'],
    '<symbol1>': ['.', '<char>', '(<alternative>)'],
    '<symbol2>': ['.', '<char>', '(<alternative>)'],
    '<symbol3>': ['.', '<char>', '(<alternative>)'],
    '<symbol4>': ['.', '<char>', '(<alternative>)'],
    '<char>': ['a', 'b', 'c'],
    '<range>': ['<num>', ',<num>'],
    '<num>': ['1', '2'],
}
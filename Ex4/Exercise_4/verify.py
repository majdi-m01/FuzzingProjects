import os
import inspect
import json
import importlib
from fuzzingbook.Grammars import is_valid_grammar

PRINT_FORMAT = '{:<40}{}'
CORRECT_STATE = 'PASS'
WRONG_STATE = 'FAIL'
INVALID_GRAMMAR_STATE = 'INVALID GRAMMAR FORMAT'
PRINT_FORMAT_VARS = '{:<40}{}{}'

files_to_verify = [
    os.path.join('examples.py'),
    os.path.join('exercise_1a.py'),
    os.path.join('exercise_1b.py'),
    os.path.join('exercise_1c.py'),
    os.path.join('exercise_2.py'),
    # path to file    
]

grammar_files = {
    os.path.join('exercise_1a.py'): "SNAKE_GRAMMAR",
    os.path.join('exercise_1b.py'): "RE_GRAMMAR",
    os.path.join('exercise_2.py'): "IBAN_GRAMMAR",
}

variables_to_verify = [
    ('examples', 'examples', list),
    ('exercise_1a', 'SNAKE_GRAMMAR', dict),
    ('exercise_1b', 'RE_GRAMMAR', dict),
    ('exercise_1c', 'Q1', int),
    ('exercise_2', 'iban_cc_len', list),
    ('exercise_2', 'IBAN_GRAMMAR', dict),
    # tuple of (package, var name)
]

functions_to_verify = [
    ('exercise_1b', 'learn_probabilities', 0),
    # tuple of (package, function name, number of args)
]

def verify_files():
    missing_files = list()
    for path in files_to_verify:
        if os.path.exists(path):
            state = CORRECT_STATE
            if path in grammar_files:
                my_module = importlib.import_module(path[:-3])
                g = getattr(my_module, grammar_files[path])
                if '<start>' not in g or not is_valid_grammar(g, '<start>'):
                        state = INVALID_GRAMMAR_STATE
        else:
            missing_files.append(path)
            state = WRONG_STATE
        print(PRINT_FORMAT.format(path, state))
    print()
    return missing_files

def verify_variables():
    missing_variables = list()
    current_package = None
    for package, variable, _type in variables_to_verify:
        reason = ""
        if current_package is None or current_package.__name__ != package:
            current_package = __import__(package)
        varaible_repr = f'{package}.{variable}'
        if variable in dir(current_package):
            var = getattr(current_package, variable)
            if type(var) == _type:
                state = CORRECT_STATE
                if varaible_repr == "exercise_1b1.lines":
                    if not all(type(x)==int for x in var) or len(var) >= 8:
                        reason = ": " + varaible_repr + " must be a list that contains only integers (at most 7 integers)"
                        state = WRONG_STATE
            else:
                reason = ": Type of variable " + varaible_repr + " must be " + str(_type) + " but is " + str(type(var))
                state = WRONG_STATE
        else:
            missing_variables.append(varaible_repr)
            state = WRONG_STATE
        print(PRINT_FORMAT_VARS.format(varaible_repr, state, reason))
    print()
    return missing_variables

def verify_functions():
    missing_functions = list()
    wrong_functions = list()
    current_package = None
    for package, function, args in functions_to_verify:
        if current_package is None or current_package.__name__ != package:
            current_package = __import__(package)
        function_repr = f'{package}.{function}'
        if function in dir(current_package):
            specs = inspect.getfullargspec(getattr(current_package, function))
            if len(specs[0]) == args:
                state = CORRECT_STATE
            else:
                wrong_functions.append(function_repr)
                state = WRONG_STATE
        else:
            missing_functions.append(function_repr)
            state = WRONG_STATE
        print(PRINT_FORMAT.format(function_repr, state))
    print()
    return missing_functions, wrong_functions

class VerificationError(ValueError):
    pass

if __name__ == '__main__':
    missing_files = verify_files()
    missing_variables = verify_variables()
    missing_functions, wrong_functions = verify_functions()
    for l, m in [(missing_files, 'Missing file'), (missing_variables, 'Missing variable'), 
                 (missing_functions, 'Missing functions'), (wrong_functions, 'Wrong function pattern')]:
        for v in l:
            print(f'{m}: {v}')
        if l:
            print()
    if missing_files or missing_variables:
        raise VerificationError()
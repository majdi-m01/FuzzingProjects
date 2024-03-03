import os
import inspect

PRINT_FORMAT = '{:<40}{}'
PRINT_FORMAT_VARS = '{:<40}{}{}'
CORRECT_STATE = 'PASS'
WRONG_STATE = 'FAIL'

files_to_verify = [
    os.path.join('exercise_1a.py'),
    os.path.join('exercise_1b.py'),
    os.path.join('exercise_1c.py'),
    os.path.join('exercise_2a.py'),
    os.path.join('exercise_2b.py'),
    # path to file    
]

variables_to_verify = [
    ('exercise_1c', 'Q1', bool),
    ('exercise_1c', 'Q2', bool),
    ('exercise_1c', 'Q3', bool),
    ('exercise_1c', 'Q4', bool),
    ('exercise_2a', 'FunctionRunner', type),
    ('exercise_2a', 'FunctionCoverageRunner', type),
    ('exercise_2b', 'RandomCoverageFuzzer', type),
    # tuple of (package, var name, type)
]

functions_to_verify = [
    ('exercise_1a', 'lcsaj', 1),
    ('exercise_1b', 'lcsaj_n', 2),
    # tuple of (package, function name, number of args)
]

def verify_files():
    missing_files = list()
    for path in files_to_verify:
        if os.path.exists(path):
            state = CORRECT_STATE
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
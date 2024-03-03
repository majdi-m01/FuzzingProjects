import os
import inspect

PRINT_FORMAT = '{:<40}{}'
CORRECT_STATE = 'PASS'
WRONG_STATE = 'FAIL'

files_to_verify = [
    os.path.join('exercise_1.py'),
    os.path.join('exercise_2.py'),
    os.path.join('server.py'),
    os.path.join('luhn.py'),
    os.path.join('test_1.py'),
    # path to file    
]

variables_to_verify = [
    ('exercise_2', 'Q1'),
    ('exercise_2', 'Q2'),
    ('exercise_2', 'Q3'),
    ('exercise_2', 'Q4'),
    ('server', 'HTML_REGISTER_FORM'),
    ('server', 'HTML_REGISTERED'),
    ('server', 'HTML_NOT_REGISTERED'),
    ('server', 'HTML_NOT_FOUND'),
    ('server', 'HTML_INTERNAL_SERVER_ERROR'),
    ('server', 'USERS_DB'),
    ('server', 'mail_pattern'),
    ('server', 'RegisterHTTPRequestHandler'),
]

functions_to_verify = [
    ('exercise_1', 'get_fuzzer', 1),
    ('test_1', 'test', 0),
    ('luhn', 'luhn', 1),
    ('server', 'init_db', 0),
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
    for package, variable in variables_to_verify:
        if current_package is None or current_package.__name__ != package:
            current_package = __import__(package)
        varaible_repr = f'{package}.{variable}'
        if variable in dir(current_package):
            state = CORRECT_STATE
        else:
            missing_variables.append(varaible_repr)
            state = WRONG_STATE
        print(PRINT_FORMAT.format(varaible_repr, state))
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

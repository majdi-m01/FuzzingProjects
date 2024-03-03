import traceback

from exercise_1 import *

def get_tainted_int():
    return tany(2, taint='int')

def get_tainted_bool():
    return tany(True, taint='bool')

def get_tainted_str():
    return tany('2', taint='str')

def get_tainted_str2():
    return tany('aBc', taint='str')

def get_tainted_list():
    return tany([1, 2, 3], taint='list')

def test(t, v, taint):
    assert t.value == v and t.taint == taint, f'Expected {(v, taint)} but was {(t.value, t.taint)}'

    
def test_add():
    x = get_tainted_int()
    y = get_tainted_str()
    test(x + 2, 4, 'int')
    test(4 + x, 6, 'int')
    test(y + '1', '21', 'str')
    test('1' + y, '12', 'str')

def test_sub():
    x = get_tainted_int()
    test(x - 2, 0, 'int')
    test(4 - x, 2, 'int')

def test_mul():
    x = get_tainted_int()
    y = get_tainted_str()
    test(x * 2, 4, 'int')
    test(4 * x, 8, 'int')
    test(y * 2, '22', 'str')
    test(3 * y, '222', 'str')

def test_div():
    x = get_tainted_int()
    test(x / 2, 1.0, 'int')
    test(4 / x , 2.0, 'int')
    test(x // 2, 1, 'int')
    test(4 // x , 2, 'int')
    test(x % 2, 0, 'int')
    test(5 % x , 1, 'int')
    test(divmod(x, 2), (1, 0), 'int')
    test(divmod(5, x) , (2, 1), 'int')

def test_shift():
    x = get_tainted_int()
    test(x << 2, 8, 'int')
    test(2 << x , 8, 'int')
    test(x >> 2, 0, 'int')
    test(2 >> x , 0, 'int')

def test_bool_ops():
    x = get_tainted_bool()
    test(x & False, False, 'bool')
    test(False & x, False, 'bool')
    test(x | False, True, 'bool')
    test(False | x, True, 'bool')
    test(x ^ False, True, 'bool')
    test(False ^ x, True, 'bool')

def test_comparison_ops():
    x = get_tainted_int()
    test(x < 2, False, 'int')
    test(x <= 2, True, 'int')
    test(x > 2, False, 'int')
    test(x <= 2, True, 'int')
    test(x == 2, True, 'int')
    test(x != 2, False, 'int')

def test_number_ops():
    x = get_tainted_int()
    test(-x, -2, 'int')
    test(+x, 2, 'int')
    test(abs(x), 2, 'int')
    test(~x, -3, 'int')
    test(round(x), 2, 'int')
    
def test_number_casts():
    x = get_tainted_str()
    test(tint(x), 2, 'str')
    test(tfloat(x), 2.0, 'str')
    test(tcomplex(tany('4-5j', taint='complex')), complex(4, -5), 'complex')
    
def test_str_casts():
    x = get_tainted_int()
    test(repr(x), '2', 'int')
    test(tstr(x), '2', 'int')
    
def test_str_ops():
    x = get_tainted_str2()
    test(x.capitalize(), 'Abc', 'str')
    test(x.casefold(), 'abc', 'str')
    test(x.center(5), ' aBc ', 'str')
    test(x.encode(), b'aBc', 'str')
    test(x.expandtabs(), 'aBc', 'str')
    test(x.format(), 'aBc', 'str')
    test(x.format_map({}), 'aBc', 'str')
    test(x.join('..'), '.aBc.', 'str')
    test(x.lower(), 'abc', 'str')
    test(x.upper(), 'ABC', 'str')
    test(x.ljust(5), 'aBc  ', 'str')
    test(x.rjust(5), '  aBc', 'str')
    test(x.lstrip('c'), 'aBc', 'str')
    test(x.rstrip('c'), 'aB', 'str')
    test(x.strip('c'), 'aB', 'str')
    test(x.replace('Bc', 'd'), 'ad', 'str')
    test(x.swapcase(), 'AbC', 'str')
    test(x.title(), 'Abc', 'str')
    test(x.startswith('aB'), True, 'str')
    test(x.split('B'), ['a', 'c'], 'str')
    
def test_str_ops2():
    x = get_tainted_str2()
    test(x.isupper(), False, 'str')
    test(x.isspace(), False, 'str')
    test(x.istitle(), False, 'str')
    test(x.isprintable(), True, 'str')
    test(x.isnumeric(), False, 'str')
    test(x.islower(), False, 'str')
    test(x.isidentifier(), True, 'str')
    test(x.isdigit(), False, 'str')
    test(x.isdecimal(), False, 'str')
    test(x.isalpha(), True, 'str')
    test(x.isalnum(), True, 'str')

def test_container_ops():
    x = get_tainted_list()
    test(len(x), 3, 'list')
    test(x[1], 2, 'list')
    i = 0
    for t in x:
        i += 1
        test(t, i, 'list')
    for t in reversed(x):
        test(t, i, 'list')
        i -= 1
    x.append(4)
    test(x[3], 4, 'list')
    test(x[1:3], [2, 3], 'list')
    
def test_container_ops2():
    x = get_tainted_list()
    x.append(4)
    x.insert(0, 0)
    test(x[0], 0, 'list')
    x.remove(0)
    test(len(x), 4, 'list')
    test(x.pop(), 4, 'list')
    test(len(x), 3, 'list')
    test(x.index(2), 1, 'list')
    test(x.index(2), 1, 'list')
    x.append(0)
    x.sort()
    test(x, [0, 1, 2, 3], 'list')
    del x[0]
    x[0] = 4
    test(x, [4, 2, 3], 'list')
    assert 3 in x

    
def main():
    tests = [test_add, test_sub, test_mul, test_div, test_shift, test_bool_ops, 
             test_comparison_ops, test_number_ops, test_number_casts, test_str_casts, 
             test_str_ops, test_str_ops2, test_container_ops, test_container_ops2]
    
    passed = 0
    for t in tests:
        print(f'{t.__name__}:', end='')
        try:
            t()
        except:
            print('FAILED')
            traceback.print_exc()
        else:
            print('PASSED')
            passed += 1
    print()
    print(f'Passed {passed}/{len(tests)}')
    return passed
    

if __name__ == '__main__':
    main()
    
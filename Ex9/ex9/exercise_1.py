from ctypes import resize
from typing import Any

ops = ['__add__', '__sub__', '__mul__', '__matmul__', '__truediv__',
       '__floordiv__', '__mod__', '__divmod__', '__pow__', '__lshift__', 
       '__rshift__', '__and__', '__xor__', '__or__', '__lt__', '__le__',
       '__gt__', '__ge__','__eq__', '__ne__']

rops = ['__radd__', '__rsub__', '__rmul__', '__rmatmul__', '__rtruediv__',
        '__rfloordiv__', '__rmod__', '__rdivmod__', '__rpow__', '__rlshift__', 
        '__rrshift__', '__rand__', '__rxor__', '__ror__', '__rlt__', '__rle__',
        '__rgt__', '__rge__','__req__', '__rne__']

number_ops = ['__neg__', '__pos__', '__abs__', '__invert__', 
             '__round__', '__int__', '__float__', '__complex__']

str_ops = ['__repr__', '__str__', 'capitalize', 'casefold', 'center', 'encode', 
           'expandtabs', 'format', 'format_map', 'join', 'ljust', 
           'lower', 'lstrip', 'replace', 'rjust', 'rstrip', 'strip', 
           'swapcase', 'title', 'translate', 'upper', 'startswith', 'split',
           'isupper', 'isspace', 'istitle', 'isprintable', 'isnumeric', 'islower',
           'isidentifier', 'isdigit', 'isdecimal', 'isalpha', 'isalnum']

container_ops = ['__len__', '__getitem__', '__iter__', '__next__', '__reversed__', 
                 '__missing__', 'append', 'extend', 'insert', 'remove', 'pop', 
                 'clear', 'index', 'count', 'sort', 'reverse', 'copy']

container_ops_unchanged = ['__setitem__', '__delitem__', '__contains__']


class tany(object):
    
    def __init__(self, value: Any, taint: Any = None, **kwargs):
        """Constructor.
        `value` is the string value the `tstr` object is to be constructed from.
        `taint` is an (optional) taint to be propagated to derived strings."""
        self. value = value
        self.taint = taint
        
    def __repr__(self):
        return self.value.__repr__()
    
    def clear_taint(self):
        """Remove taint"""
        self.taint = None
        return self

    def has_taint(self):
        """Check if taint is present"""
        return self.taint is not None
    
    def create(self, x: Any):
        # TODO: Implement this function
        return tany(x, taint=self.taint)
    
    @staticmethod
    def make_wrapper(fun_name: str):
        """Make `fun_name` from any class a method in `tany`"""
        def proxy(self, *args, **kwargs):
            args = list(args)
            for i in range(len(args)):
                if isinstance(args[i], tany):
                    args[i] = args[i].value
            for k in kwargs:
                if isinstance(kwargs[k], tany):
                    kwargs[k] = kwargs[k].value
            try:
                res = getattr(self.value, fun_name)(*args, **kwargs)
            except AttributeError:
                res = getattr(args[0], fun_name.replace('__r', '__'))(self.value, *args[1:], **kwargs) 
            return self.create(res)

        return proxy
    
    @staticmethod
    def make_wrapper_unchanged_return(fun_name: str):
        """Make `fun_name` from any class a method in `tany` but returns a not tainted object"""
        def proxy(self, *args, **kwargs):
            args = list(args)
            for i in range(len(args)):
                if isinstance(args[i], tany):
                    args[i] = args[i].value
            for k in kwargs:
                if isinstance(kwargs[k], tany):
                    kwargs[k] = kwargs[k].value
            res = getattr(self.value, fun_name)(*args, **kwargs)
            return res

        return proxy


# Wrappers
original_repr = repr
original_len = len

def repr_wrapper(x):
    if isinstance(x, tany):
        return x.create(original_repr(x.value))
    else:
        return original_repr(x)
    
    
def len_wrapper(x):
    if isinstance(x, tany):
        return x.create(original_len(x.value))
    else:
        return original_len(x)

    
repr = repr_wrapper
len = len_wrapper


# Casts    
def tint(x):
    if isinstance(x, tany):
        return x.create(int(x.value))
    else:
        return int(x)

    
def tfloat(x):
    if isinstance(x, tany):
        return x.create(float(x.value))
    else:
        return float(x)

    
def tstr(x):
    if isinstance(x, tany):
        return x.create(str(x.value))
    else:
        return str(x)
    

def tcomplex(x):
    # TODO: Implement this function
    if hasattr(x, 'value'):
        complex_x_value = complex(x.value)
    else:
        complex_x_value = complex(x)
    if isinstance(x, tany):
        return x.create(complex_x_value)
    else:
        return complex(x)

    
#TODO: Add the new functions here
for i in ops:
  setattr(tany, i, tany.make_wrapper(i))

for i in rops:
  setattr(tany, i, tany.make_wrapper(i))

for i in number_ops:
  setattr(tany, i, tany.make_wrapper(i))

for i in str_ops:
  setattr(tany, i, tany.make_wrapper(i))

for i in container_ops:
  setattr(tany, i, tany.make_wrapper(i))

for i in container_ops_unchanged:
  setattr(tany, i, tany.make_wrapper_unchanged_return(i))




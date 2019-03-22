import types
import functools


def copy_function(f, new_name):
    '''Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard) and
    https://stackoverflow.com/a/13503277/1052418 (unutbu)'''
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    g.__name__ = new_name
    return g

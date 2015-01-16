from . import eudf

import functools
import inspect

__f_increment = 0

def EUDFuncMethod(method):
    global __f_increment

    # Get argument number of fdecl_func
    argspec = inspect.getargspec(method)
    assert argspec[1] is None, (
        'No variadic arguments (*args) allowed for EUDFunc.')
    assert argspec[2] is None, (
        'No variadic keyword arguments (*kwargs) allowed for EUDFunc.')

    argn = len(argspec[0]) - 1
    idf = __f_increment
    __f_increment += 1

    def call(self, *args):
        # Create eudfuncmethod list
        if not hasattr(self, '_efmlist'):
            self._efmlist = {}

        # Create wrapper for eudfunc
        if idf not in self._efmlist:
            def call2(*args):
                return method(self, *args)
            call2 = eudf.EUDFuncN(call2, argn)
            self._efmlist[idf] = call2

        # Call that wrapper with arguments
        return self._efmlist[idf](*args)

    functools.update_wrapper(call, method)
    return call

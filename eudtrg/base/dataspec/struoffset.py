'''
ctypes struct -> offset
'''

from ctypes import *
from .expr import Expr

_class_to_offset_class = {}


def CreateOffsetMapping(ctypes_class, offset):
    '''
    Create offset calculator based on ctypes class. ::

        class A(Structure):
            _fields_ = [
                ('x', c_int),
                ('y', c_int)
            ]

        class B(Structure):
            _fields_ = [
                ('p', A * 10 * 10),
                ('q', c_int * 10 * 10),
                ('r', c_int)
            ]

        # B = template ctypes class, 0 = Offset of B instance
        x = CreateOffsetMapping(B, 0)
        print(x.p[3][5].y) # prints (284, 0)

    :param ctypes_class: Template ctypes Structure class to be used for offset
        calculation.

    :param offset: Offset of where your structure will reside in.

    :returns: Offset mapper for your structure.

    '''

    # Not array & has no fields -> Maybe c_int or something weird.
    if not (
            issubclass(ctypes_class, Array) or
            hasattr(ctypes_class, '_fields_')):
        return offset  # Return offset

    # name_type_d : member name -> member type
    # _class_name_type_dict : cache of name_type_d
    try:
        _Class_Offset = _class_to_offset_class[ctypes_class]

    except KeyError:

        # Create new class

        if issubclass(ctypes_class, Array):
            # Array class
            elmnclass = ctypes_class._type_
            elmnsize = sizeof(elmnclass)

            class _Class_Offset(Expr):

                def __init__(self, offset):
                    super().__init__()
                    self._ret = offset

                def __getitem__(self, index):
                    return CreateOffsetMapping(
                        elmnclass,
                        self + elmnsize * index
                    )

                def GetDependencyList(self):
                    return [self._ret]

                def EvalImpl(self):
                    return Evaluate(self._ret)

        else:
            name_type_d = dict([(n, t) for n, t in ctypes_class._fields_])

            class _Class_Offset(Expr):

                def __init__(self, offset):
                    super().__init__()
                    self._ret = offset

                def __getattr__(self, name):
                    mem_type = name_type_d[name]
                    mem_offset = getattr(ctypes_class, name).offset

                    return CreateOffsetMapping(
                        mem_type,
                        self + mem_offset
                    )

                def GetDependencyList(self):
                    return [self._ret]

                def EvalImpl(self):
                    return Evaluate(self._ret)

        _class_to_offset_class[ctypes_class] = _Class_Offset

    return _Class_Offset(offset)

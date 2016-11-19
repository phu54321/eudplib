cdef class RlocInt_C:
    cdef public unsigned int offset, rlocmode

cpdef RlocInt_C RlocInt(offset, rlocmode)
cpdef RlocInt_C toRlocInt(x)
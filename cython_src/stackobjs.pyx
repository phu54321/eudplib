from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from libc.string cimport memset

def StackObjects(
    found_objects,
    dwoccupmap_dict,
    alloctable,
):
    cdef int dwoccupmap_max_size = 0
    for obj in found_objects:
        dwoccupmap_max_size += obj.GetDataSize()

    # Buffer to sum all dwoccupmaps
    cdef int* dwoccupmap_sum = <int*> PyMem_Malloc((dwoccupmap_max_size + 1) * sizeof(int))
    cdef int* dwoccupmap = <int*> PyMem_Malloc((dwoccupmap_max_size + 1) * sizeof(int))
    memset(dwoccupmap_sum, -1, (dwoccupmap_max_size + 1) * sizeof(int))

    cdef int lallocaddr = 0
    cdef int payload_size = 0
    cdef int curoff, objsize, j, oclen

    for obj in found_objects:
        py_dwoccupmap = dwoccupmap_dict[obj]
        oclen = len(py_dwoccupmap)
        for j in range(oclen):
            dwoccupmap[j] = py_dwoccupmap[j]

        # Find appropriate position to allocate object
        j = 0
        while j < oclen:
            # Update on conflict map
            if dwoccupmap[j] != -1 and dwoccupmap_sum[lallocaddr + j] != -1:
                lallocaddr = dwoccupmap_sum[lallocaddr + j] - dwoccupmap[j]
                j = 0

            else:
                j += 1

        # Apply occupation map
        for j in range(oclen - 1, -1, -1):
            curoff = lallocaddr + j
            if dwoccupmap[j] != -1 or dwoccupmap_sum[curoff] != -1:
                if dwoccupmap_sum[curoff + 1] == -1:
                    dwoccupmap_sum[curoff] = curoff + 1
                else:
                    dwoccupmap_sum[curoff] = dwoccupmap_sum[curoff + 1]

        objsize = obj.GetDataSize()
        alloctable[obj] = (lallocaddr * 4, objsize)
        if lallocaddr * 4 + objsize > payload_size:
            payload_size = lallocaddr * 4 + objsize

    PyMem_Free(dwoccupmap)
    PyMem_Free(dwoccupmap_sum)


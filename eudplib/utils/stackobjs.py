

def StackObjects(
    found_objects,
    dwoccupmap_dict,
    alloctable,
):
    dwoccupmap_max_size = 0
    for obj in found_objects:
        dwoccupmap_max_size += len(dwoccupmap_dict[obj])

    # Buffer to sum all dwoccupmaps
    dwoccupmap_sum = [-1] * (dwoccupmap_max_size + 1)
    dwoccupmap = [0] * (dwoccupmap_max_size + 1)
    lallocaddr = 0
    payload_size = 0

    for obj in found_objects:
        # Convert to faster c array
        py_dwoccupmap = dwoccupmap_dict[obj]
        oclen = len(py_dwoccupmap)
        for j in range(oclen):
            dwoccupmap[j] = py_dwoccupmap[j]

        # preprocess dwoccupmap
        for i in range(oclen):
            if dwoccupmap[i] == 0:
                dwoccupmap[i] = -1
            elif i == 0 or dwoccupmap[i - 1] == -1:
                dwoccupmap[i] = i
            else:
                dwoccupmap[i] = dwoccupmap[i - 1]

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

        alloctable[obj] = lallocaddr * 4
        if (lallocaddr + oclen) * 4 > payload_size:
            payload_size = (lallocaddr + oclen) * 4

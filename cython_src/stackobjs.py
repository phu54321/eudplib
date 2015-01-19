
def StackObjects(
    found_objects,
    dwoccupmap_dict,
    alloctable,
    dsdict,
):
    dwoccupmap_max_size = 0
    for obj in found_objects:
        dwoccupmap_max_size += dsdict[obj]

    # Buffer to sum all dwoccupmaps
    dwoccupmap_sum = [-1] * (dwoccupmap_max_size + 1)

    lallocaddr = 0
    payload_size = 0

    for obj in found_objects:
        dwoccupmap = dwoccupmap_dict[obj]

        # Find appropriate position to allocate object
        j = 0
        oclen = len(dwoccupmap)
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

        alloctable[obj] = (lallocaddr * 4, dsdict[obj])
        objsize = dsdict[obj]
        if lallocaddr * 4 + objsize > payload_size:
            payload_size = lallocaddr * 4 + objsize

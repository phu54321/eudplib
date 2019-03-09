import pyximport

pyximport.install()

from stackobjs import StackObjects

found_objects = [1, 2, 3, 4, 5]
dwoccupmap_dict = {
    1: [0, 1, 1, 0, 0, 1],
    2: [0, 0, 0, 0, 0, 1],
    3: [1, 1, 1, 1, 1, 1],
    4: [0, 1, 0, 0, 0, 0],
    5: [2, 2, 2, 2, 2, 2],
}
alloctable = {}

StackObjects(found_objects, dwoccupmap_dict, alloctable)

print(alloctable)

for obj in found_objects:
    s = []
    s.append("%4s: " % obj)
    s.append(" " * (alloctable[obj] // 4))
    dwoccupmap = dwoccupmap_dict[obj]
    for j in dwoccupmap:
        if j:
            s.append("#")
        else:
            s.append(" ")

    print("".join(s))

'''
Dependency graph library. Traverses through objects by dependencies, collecting
required objects. Used internally in eudtrg.
'''

from eudtrg import LICENSE  # @UnusedImport

# Dependency graph library
from ..dataspec.eudobj import EUDObject
from ..dataspec.expr import GetDependencyList


def GetAllDependencies(root):
    traversed = set()
    deplist = []

    stack = [root]

    while stack:
        node = stack.pop()
        if node in traversed:
            continue

        traversed.add(node)
        # dependent items have their addresses determined by other independent
        # item.
        if isinstance(node, EUDObject):
            deplist.append(node)

        stack.extend(
            [x for x in GetDependencyList(node) if x not in traversed])

    return deplist

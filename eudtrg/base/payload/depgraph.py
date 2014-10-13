'''
Dependency graph library. Traverses through objects by dependencies, collecting
required objects. Used internally in eudtrg.
'''

'''
Copyright (c) 2014 trgk

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
   3. This notice may not be removed or altered from any source
   distribution.
'''

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

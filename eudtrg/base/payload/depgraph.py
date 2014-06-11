"""
Dependency graph library. Traverses through objects by dependencies, collecting
needed objects. Used internally in eudtrg.
"""

# Dependency graph library
from ..dataspec import addressable
from ..dataspec import expr

class DependencyGraphNode:
	def __init__(self):
		pass

	def GetDependencyList(self):
		raise NotImplementedError('Pure virtual function')


def IsIndependent(item):
	if isinstance(item, addressable.Addressable):
		return item.IsIndependent()
	
	else:
		return False


def GetDependencyList(item):
	if isinstance(item, addressable.Addressable):
		return item.GetDependencyList()

	elif isinstance(item, addressable.Addr):
		return [item.target]

	elif isinstance(item, expr.BinopExpr):
		return GetDependencyList(item.exprA) + GetDependencyList(item.exprB)

	else:
		return []


def GetAllDependencies(root):
	traversed = set()
	deplist = []
		
	stack = [root]

	while stack:
		node = stack.pop()
		if node in traversed: continue
		
		traversed.add(node)
		# dependent items have their addresses determined by other independent item.
		if IsIndependent(node):
			deplist.append(node)
			
		stack.extend(GetDependencyList(node))

	return deplist
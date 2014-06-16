"""
Useful utilities. You may freely use these functions.
"""

"""
offset -> EPD player number according to offset
"""
def EPD(offset):
	return (offset - 0x0058A364) // 4


def FlattenList(l):
	ret = []
	try:
		for item in l:
			ret.extend(FlattenList(item))

	except TypeError: # l is not iterable
		ret.append(l)
			
	return ret
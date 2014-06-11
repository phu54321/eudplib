"""
Useful utilities. You may freely use these functions.
"""

"""
offset -> EPD player number according to offset
"""
def EPD(offset):
	return (offset - 0x0058A364) // 4


"""
nested list -> flatten
ex) [[1, 2], [3, [4, 5], 6], 7] -> [1, 2, 3, 4, 5, 6, 7]
Trigger class uses this function to unlap nested condition/actions, so pattern
	[
		[
			SetDeaths(1, 2, 3, 4),
			SetDeaths(5, 6, 7, 8)
		],
		SetSwitch(1, Set)
	]
is possible.
"""

def FlattenList(l):
	ret = []
	for item in l:
		try:
			ret.extend(FlattenList(item))
		except: # item cannot be flattened. Maybe already flattened?
			ret.append(item)
			
	return ret

"""
Useful utilities. You may freely use these functions.
"""

"""
offset -> EPD player number according to offset
"""
def EPD(offset):
	return (offset - 0x0058A364) // 4


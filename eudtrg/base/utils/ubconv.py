"""
Unicode(python) <-> Binary(starcraft) conversion. Used internally in eudtrg.
"""

import sys

# This works for me. If anything goes wrong, change below.
charset = sys.stdin.encoding

def Unicode2Bytes(string):
	return string.encode(charset)

def Bytes2Unicode(b):
	return b.decode(charset)
	
def main():
	print("Performing unicode - multibyte conversion library")

if __name__ == "__main__":
	main()

# shorter names
u2b = Unicode2Bytes
b2u = Bytes2Unicode
import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *


LoadMap('outputmap/basemap/basemap.scx')
MPQAddFile('testmpqfile.py', open('testmpqfile.py', 'rb').read())
MPQAddFile('testmpqfile.py', open('testmpqfile.py', 'rb').read())  # Error!


@EUDFunc
def main():
    pass

SaveMap('outputmap\\testmpqf.scx', main)

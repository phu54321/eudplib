import sys
import os
import pprint as pp

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

pp.pprint(GetInlineCodeNamespace())

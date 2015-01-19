from distutils.core import setup
from Cython.Build import cythonize

import sys

sys.argv.extend(['build_ext', '--inplace'])

setup(
    name='My hello app',
    ext_modules=cythonize('*.pyx'),
)

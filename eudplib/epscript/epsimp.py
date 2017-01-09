from importlib.machinery import (
    FileFinder,
    SourceFileLoader,
)

from .epscompile import epsCompile
from eudplib.utils import EPError
import sys


class EPSLoader(SourceFileLoader):
    def __init__(self, *args):
        super().__init__(*args)

    def get_data(self, path):
        """Return the data from path as raw bytes."""
        fileData = open(path, 'rb').read()
        if path.endswith('.pyc') or path.endswith('.pyo'):
            return fileData
        compiled = epsCompile(path, fileData)
        if compiled is None:
            raise EPError('epScript compiled failed for %s' % path)
        return compiled


class EPSFinder:
    def __init__(self):
        self._finderCache = {}

    def _getFinder(self, path):
        try:
            return self._finderCache[path]
        except KeyError:
            self._finderCache[path] = FileFinder(path, (EPSLoader, ['.eps']))
            return self._finderCache[path]

    def find_spec(self, fullname, path, target=None):
        if path is None:
            path = sys.path
        for pathEntry in path:
            finder = self._getFinder(pathEntry)
            spec = finder.find_spec(fullname)
            if spec is None:
                continue
            return spec


sys.meta_path.append(EPSFinder())

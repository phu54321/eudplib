import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    f_initextstr()

    f_setcurpl(Player1)

    DoActions([
        DisplayText('a'),
        DisplayExtText('Hello world!'),
        DisplayExtText('Hello world!'),
        DisplayExtText('Bye world!'),
        DisplayExtText('Hello world!'),
        DisplayExtText(
            'afafgafafafafafgafafafafafgafafafafafgafafafafafgafafafafafgafafafafafgafafafafafgafafafafafgafafaf'),
        DisplayText('a'),
    ])


SaveMap('outputmap/testextstr.scx', main)

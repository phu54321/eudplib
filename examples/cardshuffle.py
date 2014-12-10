'''
simple eudtrg importer
'''

import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

cards = EUDArray(54)


def ShuffleArray(arr, n):
    ''' Array shuffler
    :param EUDArray arr: Array to shuffle
    :param n: Number of elements insode array
    '''
    i = EUDVariable()
    t = EUDVariable()
    i << 0

    if EUDWhile(i < n):
        j = i + f_div(f_rand(), n - i)[1]
        t << arr.get(i)
        arr.set(i, arr.get(j))
        arr.set(j, t)
        i << i + 1
    EUDEndWhile()


@EUDFunc
def PrepareDeck():
    for i in range(54):
        cards.set(i, i)

    ShuffleArray(cards, 54)


def main():
    PrepareDeck()
    for i in range(54):
        SeqCompute([(EPD(0x58D740) + i, SetTo, cards.get(i))])


LoadMap('basemap/basemap.scx')
# CompressPayload(True)
SaveMap('outputmap/shuffle.scx', main)

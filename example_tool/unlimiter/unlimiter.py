from eudplib import *
import sys, os

'''
총알 갯수         : 100 -> 65536
스프라이트 갯수   : 2500 -> 65536
이미지 갯수       : 5000 -> 65536
발키리가 최대한 잘 쏘도록 계속 패치
'''


def ConnectDList(emptylist_start, emptylist_end, itemsize, itemn):
    liststart = Db(bytes(itemsize * itemn))
    DoActions(SetDeaths(0, SetTo, liststart, 0))
    _ConnectDList(EPD(emptylist_start), EPD(emptylist_end), liststart, EPD(liststart), itemsize, itemsize // 4, itemn)


@EUDFunc
def _ConnectDList(emptylist_start_epd, emptylist_end_epd, liststart, liststart_epd, itemsize, itemsize_div4, itemn):
    ols, olsepd = EUDVariable(), EUDVariable()
    ols << liststart
    olsepd << liststart_epd

    if EUDWhile(itemn > 0):
        f_dwwrite_epd(liststart_epd, liststart - itemsize)
        f_dwwrite_epd(liststart_epd + 1, liststart + itemsize)
        liststart += itemsize
        liststart_epd += itemsize_div4
        itemn -= 1
    EUDEndWhile()

    liststart_epd -= itemsize_div4
    liststart -= itemsize
    f_dwwrite_epd(olsepd, 0)
    f_dwwrite_epd(liststart_epd + 1, 0)
    f_dwwrite_epd(emptylist_start_epd, ols)
    f_dwwrite_epd(emptylist_end_epd, liststart)


'''
void ValkyrieFix() {
    *(DWORD*)0x64DEBC = 40;
}
'''


def inj_main():
    ConnectDList(0x64EED8, 0x64EEDC, 112, 65536)  # 총알 갯수 패치
    ConnectDList(0x63FE30, 0x63FE34, 36, 65536)  # 스프라이트 갯수 패치
    ConnectDList(0x57EB68, 0x57EB70, 64, 65536)  # 이미지 갯수 패치

    if EUDInfLoop():
        RunTrigTrigger()
        DoActions(SetMemory(0x64DEBC, SetTo, 40))  # Valkyrie fix
        EUDDoEvents()
    EUDEndInfLoop()


if len(sys.argv) != 2:
    print('Usage : unlimiter [input map]')
    os.system('Pause')
    sys.exit()

ifname = sys.argv[1]
if ifname[-4:] != '.scx':
    print("Map extension should be '.scx'")
    os.system('Pause')
    sys.exit()

LoadMap(ifname)
SaveMap(ifname[:-4] + ' ulm.scx', inj_main)

print('Complete')

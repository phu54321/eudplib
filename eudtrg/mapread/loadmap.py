from ..core.mapdata import chktok, mpqapi, mapdata


def LoadMap(fname):
    print('Loading map %s' % fname)
    rawfile = open(fname, 'rb').read()
    mpqr = mpqapi.MpqRead()
    mpqr.Open(fname)
    chkt = chktok.CHK(mpqr.Extract('staredit\\scenario.chk'))
    mapdata.InitMapData(chkt, rawfile)

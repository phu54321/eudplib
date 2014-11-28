from ..core.mapdata import mapdata, mpqapi


def SaveMap(fname, root):
    mapdata.UpdateMapData()
    chkt = mapdata.GetChkTokenized()

    # TODO : Inject triggers here

    rawchk = chkt.savechk(chkt)

    open(fname, 'wb').write(mapdata.GetRawFile())

    mw = mpqapi.MpqWrite()
    mw.Open(fname)
    mw.PutFile('staredit\\scenario.chk', rawchk)
    mw.Compact()
    mw.Close()

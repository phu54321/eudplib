from .. import core as c
from ..core.mapdata import mapdata, mpqapi
from .injector import stage1, stage2, stage3, doevents


def SaveMap(fname, rootf):
    mapdata.UpdateMapData()
    chkt = mapdata.GetChkTokenized()

    # Create injector triggers
    root = doevents._MainStarter(rootf)
    root = stage3.CreateStage3(root)
    payload = c.CreatePayload(root)
    final_payload = stage2.CreateStage2(payload)
    stage1.CreateAndApplyStage1(chkt, final_payload)

    rawchk = chkt.savechk(chkt)

    open(fname, 'wb').write(mapdata.GetRawFile())

    mw = mpqapi.MpqWrite()
    mw.Open(fname)
    mw.PutFile('staredit\\scenario.chk', rawchk)
    mw.Compact()
    mw.Close()

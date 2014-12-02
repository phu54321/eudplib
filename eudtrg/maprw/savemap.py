from .. import core as c
from .. import varfunc as vf
from ..core.mapdata import mapdata, mpqapi
from .injector import stage1, stage2, stage3, doevents


def SaveMap(fname, rootf):
    print('Saving to %s...' % fname)
    chkt = mapdata.GetChkTokenized()

    # Create injector triggers
    bsm = c.BlockStruManager()
    prev_bsm = c.SetCurrentBlockStruManager(bsm)
    old_evb = vf.SetCurrentVariableBuffer(vf.EUDVarBuffer())

    c.PushTriggerScope()
    root = doevents._MainStarter(rootf)
    root = stage3.CreateStage3(root)
    c.PopTriggerScope()
    payload = c.CreatePayload(root)

    vf.SetCurrentVariableBuffer(vf.EUDVarBuffer())

    c.PushTriggerScope()
    final_payload = stage2.CreateStage2(payload)
    c.PopTriggerScope()
    vf.SetCurrentVariableBuffer(old_evb)
    c.SetCurrentBlockStruManager(prev_bsm)

    # Update string table & etc
    # rootf can be EUDFunc, which can be evaluated later.
    # User-defined strings inside eudtrg program is registered after rootf is
    # called, when _MainStarter is called. So, UpdateMapData function should
    # be called after `doevents._MainStarter(rootf)` call.
    # Moreover, since it won't matter anyway, we update string table and
    # property table after stage 2 is initialized.
    mapdata.UpdateMapData()
    # stage1.CreateAndApplyStage1 requires STR section to be constructed before
    # it append stage2 payload after 'original' STR section. so UpdateMapData
    # should be called before `stage1.CreateAndApplyStage1`.

    # Create and apply stage 1 payload.
    # Stage 1 initializes stage 2 (real payload initializer)
    stage1.CreateAndApplyStage1(chkt, final_payload)

    rawchk = chkt.savechk()
    print('Output scenario.chk : %.3fMB' % (len(rawchk) / 1000000))

    open(fname, 'wb').write(mapdata.GetRawFile())

    mw = mpqapi.MpqWrite()
    mw.Open(fname)
    mw.PutFile('staredit\\scenario.chk', rawchk)
    mw.Compact()
    mw.Close()

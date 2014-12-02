''' Stage 2 :
- Initialize payload (stage3+ + user code) & execute it
'''


from ... import core as c
from ... import stdfunc as sf
from ... import ctrlstru as cs
from ... import varfunc as vf


def CreateStage2(payload):
    # We first build code injector.
    prtdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.prttable]))
    prtn = vf.EUDVariable()

    ortdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.orttable]))
    ortn = vf.EUDVariable()

    orig_payload = c.Db(payload.data)

    c.PushTriggerScope()

    root = c.NextTrigger()

    prtn << len(payload.prttable)
    ortn << len(payload.orttable)

    # init prt
    if payload.prttable:
        if cs.EUDInfLoop():
            cs.DoActions(prtn.SubtractNumber(1))
            sf.f_dwadd_epd(
                c.EPD(orig_payload) + sf.f_dwread_epd(prtn + c.EPD(prtdb)),
                orig_payload // 4
            )
            cs.EUDLoopBreakIf(prtn.Exactly(0))
        cs.EUDEndInfLoop()

    # init ort
    if payload.orttable:
        if cs.EUDInfLoop():
            cs.DoActions(ortn.SubtractNumber(1))
            sf.f_dwadd_epd(
                c.EPD(orig_payload) + sf.f_dwread_epd(ortn + c.EPD(ortdb)),
                orig_payload
            )
            cs.EUDLoopBreakIf(ortn.Exactly(0))
        cs.EUDEndInfLoop()

    # Jump
    cs.EUDJump(orig_payload)

    c.PopTriggerScope()

    ####
    # return c.CreatePayload(root)
    ####

    payload = c.CreatePayload(root)
    open('out.bin', 'wb').write(payload.data)
    return payload

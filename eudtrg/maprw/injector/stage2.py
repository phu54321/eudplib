''' Stage 2 :
- Initialize payload (stage3+ + user code) & execute it
'''


from ... import core as c
from ... import stdfunc as sf
from ... import ctrlstru as cs
from ... import varfunc as vf


def GenerateStage2(payload):
    # We first build code injector.
    prtdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.prttable]))
    prtn = vf.EUDLightVariable(len(payload.prttable))

    ortdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.orttable]))
    ortn = vf.EUDLightVariable(len(payload.orttable))

    orig_payload = c.Db(payload.data)

    c.PushTriggerScope()

    root = c.NextTrigger()

    # init prt
    if cs.EUDInfLoop():
        cs.DoActions(prtn.SubtractNumber(1))
        sf.f_dwadd_epd(
            sf.f_dwread_epd(c.EPD(prtdb) + prtn) + c.EPD(orig_payload),
            (orig_payload // 4)
        )
        cs.EUDLoopBreakIf(prtn.Exactly(0))
    cs.EUDEndInfLoop()

    # init ort
    if cs.EUDInfLoop():
        cs.DoActions(ortn.SubtractNumber(1))
        sf.f_dwadd_epd(
            sf.f_dwread_epd(c.EPD(ortdb) + ortn) + c.EPD(orig_payload),
            orig_payload
        )
        cs.EUDLoopBreakIf(ortn.Exactly(0))
    cs.EUDEndInfLoop()

    # Jump
    cs.EUDJump(orig_payload)

    c.PopTriggerScope()

    return c.CreatePayload(root)

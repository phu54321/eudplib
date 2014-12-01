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

    c.Trigger(actions=c.SetDeaths(4, c.SetTo, 0x1000, 0))
    c.Trigger(actions=c.SetDeaths(4, c.SetTo, 0x2000, 0))
    c.Trigger(actions=c.SetDeaths(4, c.SetTo, 0x3000, 0))

    prtn << len(payload.prttable)
    ortn << len(payload.orttable)

    c.Trigger(actions=c.SetDeaths(4, c.SetTo, 0x4000, 0))

    # prtn << len(payload.prttable)
    # ortn << len(payload.orttable)

    # init prt
    if cs.EUDInfLoop():
        c.Trigger(actions=c.SetDeaths(4, c.Add, 0x100, 0))
        cs.DoActions(prtn.SubtractNumber(1))
        c.Trigger(actions=c.SetDeaths(4, c.Add, 0x100, 0))
        print('aaaaa')
        iaddr = prtn + c.EPD(prtdb)
        print('aaaaa')
        c.Trigger(actions=c.SetDeaths(4, c.Add, 0x100, 0))
        tp = c.EPD(orig_payload) + sf.f_dwread_epd(iaddr)
        v = orig_payload // 4

        c.Trigger(actions=c.SetDeaths(4, c.Add, 0x100, 0))

        act = c.Forward()
        vf.SeqCompute([(c.EPD(act + 16), c.SetTo, tp)])
        c.Trigger(actions=c.SetDeaths(4, c.Add, 0x400, 0))
        cs.DoActions(act << c.SetMemory(0, c.Add, v))

        '''
        sf.f_dwadd_epd(
            c.EPD(orig_payload) + sf.f_dwread_epd(prtn + c.EPD(prtdb)),
            (orig_payload // 4)
        )
        '''

        c.Trigger(actions=c.SetDeaths(4, c.Add, 0x500, 0))
        cs.EUDLoopBreakIf(prtn.Exactly(0))
    cs.EUDEndInfLoop()

    # init ort
    if cs.EUDInfLoop():
        cs.DoActions(ortn.SubtractNumber(1))
        sf.f_dwadd_epd(
            c.EPD(orig_payload) + sf.f_dwread_epd(ortn + c.EPD(ortdb)),
            orig_payload
        )
        cs.EUDLoopBreakIf(ortn.Exactly(0))
    cs.EUDEndInfLoop()

    c.Trigger(actions=c.SetDeaths(4, c.SetTo, 0x1001, 0))

    # Jump
    cs.EUDJump(orig_payload)

    c.PopTriggerScope()

    ####
    # return c.CreatePayload(root)
    ####

    payload = c.CreatePayload(root)
    open('out.bin', 'wb').write(payload.data)
    print(payload.prttable)
    print(payload.orttable)
    return payload

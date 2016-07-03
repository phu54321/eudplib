from .. import core as c


class EUDCoroutine(c.EUDStruct):
    _fields_ = [
        'callhead',
        'callend',
        'coroutineend',
        'jumper'
    ]

    def __init__(self, basefunc):
        callhead = c.Forward()
        callend = c.Forward()
        coroutineEnd = c.Forward()
        jumper = c.Forward()

        super().__init__(

        if c.PushTriggerScope():
            jumper << c.RawTrigger()
            callhead << c.NextTrigger()
            basefunc()
            callend << c.RawTrigger(actions=[
                c.SetNextPtr(jumper, callend)
            ])

        c.PushTriggerScope()
        self._jumper = c.RawTrigger(st)
        c.PopTriggerScope()


def EUDYield():


class EUDCoroutine(c.EUDStruct):
    _fields_ = [
        jumper,
        finished,
    ]

    def __init__(self, basefunc):


    def finished():
        return self.finished

    def reset():
        pass

    def run():
        pass


jumper = None


def _MainStarter(mf):
    global jumper
    jumper = c.Forward()

    if c.PushTriggerScope():
        rootstarter = c.NextTrigger()

        _f_initextstr()
        sf.f_getcurpl()  # Nessecary. See comments on f_getcurpl

        mf()

        c.RawTrigger(
            nextptr=0x80000000,
            actions=c.SetNextPtr(jumper, 0x80000000)
        )
        jumper << c.RawTrigger(nextptr=rootstarter)

    c.PopTriggerScope()

    return jumper


def EUDDoEvents():
    oldcp = sf.f_getcurpl()

    _t = c.Forward()
    cs.DoActions(c.SetNextPtr(jumper, _t))
    cs.EUDJump(0x80000000)
    _t << c.NextTrigger()

    sf.f_setcurpl(oldcp)

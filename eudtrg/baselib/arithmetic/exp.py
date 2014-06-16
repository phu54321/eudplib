from ...base import *
from ..eudfunc import EUDFunc
from ..vtable import EUDVTable
from ..varassign import SetVariables, SeqCompute
from ..ctrlstru import EUDJumpIf, EUDJumpIfNot, EUDJump
from .muldiv import f_mul, f_div


f_exp = None

def _f_exp_init():
	global f_exp

	vt = EUDVTable(3)
	a, b, ret = vt.GetVariables()
	f_exp_begin, f_exp_end = Forward(), Forward()
	f_exp = EUDFunc(f_exp_begin, f_exp_end, vt, 2, 1)

	expvt = EUDVTable(32)
	expvar = expvt.GetVariables()

	PushTriggerScope()
	f_exp_begin << NextTrigger()

	
	chain    = [Forward() for _ in range(32)]
	SetVariables([ret, expvar[0]], [1, a])

	SeqCompute((
		(ret, SetTo, 1),
		(expvar[0], SetTo, a)
	))

	for i in range(1, 31):
		EUDJumpIf(expvar[i - 1].Exactly(0), chain[i - 1])
		EUDJumpIf(b.AtMost(2**i - 1), chain[i - 1])

		SetVariables(expvar[i], f_mul.call(expvar[i - 1], expvar[i - 1]))

		skipcond_skip = Forward()
		EUDJumpIfNot(expvar[i].Exactly(1), skipcond_skip)

		SetVariables(b, f_div.call(b, 2**i)[1])
		EUDJump(chain[i - 1])

		skipcond_skip << NextTrigger()


	for i in range(31, -1, -1):
		chain[i] << NextTrigger()

		mul_skip = Forward()
		EUDJumpIfNot(b.AtLeast(2**i), mul_skip)

		SeqCompute((
			(b, Subtract, 2**i),
			(ret, SetTo, f_mul.call(ret, expvar[i]))
		))

		mul_skip << NextTrigger()


	f_exp_end << Trigger()
	PopTriggerScope()

_f_exp_init()
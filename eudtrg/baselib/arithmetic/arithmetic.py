from ..base import *
from .eudfunc import EUDFunc
from .vtable import EUDVTable, VTProc
from .varassign import SetVariables
from .ctrlstru import EUDJumpIf

f_add, f_sub, f_div, f_mul, f_exp = None, None, None, None, None
f_bitand ,f_bitor, f_bitxor = None, None, None
f_bitnot, f_bitlsft, f_bitrsft = None, None, None
f_logicand, f_logicor, f_logicnot = None, None, None
f_cmpeq, f_cmpneq, f_cmpge, f_cmple, f_cmpg, f_cmpl = None, None, None, None, None, None



# chain unit. Used internally in various arithmetic operations



def _f_lshift_init():
	global f_lshift

	vt = EUDVTable(3)
	a, b, ret = vt.GetVariables()
	f_lshift_begin, f_lshift_end = Forward(), Forward()
	f_lshift = EUDFunc(f_lshift_begin, f_lshift_end, vt, 2, 1)

	PushTriggerScope()

	# b >= 32 -> skip and return 0
	skip_if_too_large = Forward()
	EUDJumpIf(b.AtLeast(32), skip_if_too_large)

	loopbegin, loopend = Forward(), Forward()
	EUDWhile(b.AtLeast(1), loopbegin, loopend)

	if 1:
		loopbegin << NextTrigger()
		SetVariable([a, b], [a, 1], [Add, Subtract])
		loopend << Trigger()

	SetVariable(ret, a)
	EUDJump(f_lshift_end)

	skip_if_too_large << NextTrigger()
	DoActions(ret.SetNumber(0))

	f_lshift_end << Trigger()

	PopTriggerScope()

_f_lshift_init()




def _f_rshift_init():
	global f_rshift

	vt = EUDVTable(3)
	a, b, ret = vt.GetVariables()
	f_rshift_begin, f_rshift_end = Forward(), Forward()
	f_rshift = EUDFunc(f_rshift_begin, f_rshift_end, vt, 2, 1)
	
	PushTriggerScope()

	f_rshift_begin << NextTrigger()
	SetVariable(ret, f_div.call(a, f_lshift.call(1, b))[0])
	f_rshift_end << Trigger()

_f_rshift_init()


from ...base import *
from ..eudfunc import EUDFunc
from ..vtable import EUDVTable, VTProc
from ..varassign import SeqCompute

f_add = f_sub = None

# def for f_add
def _f_add_init():
	global f_add
	
	vt = EUDVTable(3)
	a, b, ret = vt.GetVariables()
	f_add_begin, f_add_end = Forward(), Forward()
	f_add = EUDFunc(f_add_begin, f_add_end, vt, 2, 1)

	PushTriggerScope()
	f_add_begin << NextTrigger()
	SeqCompute((
		(ret, SetTo, a),
		(ret, Add, b)
	))
	f_add_end << Trigger()
	PopTriggerScope()

_f_add_init()




# def for f_sub
def _f_sub_init():
	global f_sub

	vt = EUDVTable(4)
	a, b, ret, invb = vt.GetVariables()
	f_sub_begin, f_sub_end = Forward(), Forward()
	f_sub = EUDFunc(f_sub_begin, f_sub_end, vt, 2, 1)

	PushTriggerScope()
	f_sub_begin << NextTrigger()
	SeqCompute((
		(invb, SetTo, 0xFFFFFFFF),
		(invb, Subtract, b),
		(invb, Add, 1),
		(ret, SetTo, a),
		(ret, Add, invb)
	))
	f_sub_end << Trigger()
	PopTriggerScope()

_f_sub_init()
	

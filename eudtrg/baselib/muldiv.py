from ..base import *
from . import eudfunc, vtable

f_div = None
f_mul = None

def _initarith():
	global f_mul, f_div
	vt = vtable.EUDVTable(7)
	a, b, ret, remainder, x0, x1, y0 = vt.GetVariables()
	
	# declaration for f_mul, f_div
	# code from http://blog.naver.com/whyask37/140209918770
	chain_x0 = [Forward() for _ in range(32)]
	chain_x1 = [Forward() for _ in range(32)]
	chain_y0 = [Forward() for _ in range(32)]
	chain = [Forward() for _ in range(32)]
	
	
	# f_mul
	f_mul_chain_init0 = [Forward() for _ in range(32)]
	f_mul_chain_init1 = [Forward() for _ in range(32)]
	f_mul_begin = Forward()
	f_mul_finalize = Forward()
	f_mul = eudfunc.EUDFunc(f_mul_begin, f_mul_finalize, vt, 2, 1)
	
	
	f_mul_begin << Trigger(
		nextptr = vt,
		actions = [
			ret.SetNumber(0),
			x0.SetNumber(1),
			x1.SetNumber(1),
			b.QueueAssignTo(y0),
			SetNextPtr(vt, f_mul_chain_init0[31])
		]
	)
	
	for i in range(31, -1, -1):
		f_mul_chain_init0[i] << Trigger(
			nextptr = vt,
			actions = [
				x0.QueueAssignTo(EPD(chain_x0[i])),
				x1.QueueAssignTo(EPD(chain_x1[i])),
				y0.QueueAssignTo(EPD(chain_y0[i])),
				SetNextPtr(vt, f_mul_chain_init1[i])
			]
		)
	
	for i in range(31, 0, -1):
		f_mul_chain_init1[i] << Trigger(
			nextptr = vt,
			actions = [
				x0.QueueAddTo(x0),
				x1.QueueAddTo(x1),
				y0.QueueAddTo(y0),
				SetNextPtr(vt, f_mul_chain_init0[i - 1])
			]
		)
		
	f_mul_chain_init1[0] << Trigger(
		nextptr = chain[0],
		actions = [
			SetNextPtr(chain[31], f_mul_finalize),
		]
	)
	
	f_mul_finalize << Trigger()
	
	
	
	# f_div impl
	
	f_div_begin = Forward()
	f_div_1 = Forward()
	f_div_finalize1 = Forward()
	f_div_finalize2 = Forward()
	f_div_chain_init0 = [Forward() for _ in range(32)]
	f_div_chain_init1 = [Forward() for _ in range(32)]
	f_div_chain_init2 = [Forward() for _ in range(32)]
	
	f_div = eudfunc.EUDFunc(f_div_begin, f_div_finalize2, vt, 2, 2)
	
	f_div_begin << Trigger(
		nextptr = vt,
		actions = [
			ret.SetNumber(0),
			y0.SetNumber(1),
			b.QueueAssignTo(x0),
			SetNextPtr(vt, f_div_1)
		]
	)
	
	f_div_1 << Trigger(
		nextptr = vt,
		actions = [
			b.QueueAssignTo(x1),
			SetNextPtr(chain[31], f_div_finalize1),
			SetNextPtr(vt, f_div_chain_init0[31])
		]
	)
	
	# assign x, y to chain
	for i in range(31, -1, -1):
		f_div_chain_init0[i] << Trigger(
			nextptr = vt,
			actions = [
				x0.QueueAssignTo(EPD(chain_x0[i])),
				x1.QueueAssignTo(EPD(chain_x1[i])),
				y0.QueueAssignTo(EPD(chain_y0[i])),
				SetNextPtr(vt, f_div_chain_init1[i])
			]
		)
	
	# x0 >= 0x80000000 -> jump to chain
	for i in range(31, -1, -1):
		f_div_chain_init1[i] << Trigger(
			nextptr = f_div_chain_init2[i],
			conditions = [
				x0.AtLeast(0x80000000)
			],
			actions = [
				SetNextPtr(f_div_chain_init1[i], chain[i])
			]
		)
		
	# x0 += x0, x1 += x1, y0 += y0
	
	for i in range(31, 0, -1):
		f_div_chain_init2[i] << Trigger(
			nextptr = vt,
			actions = [
				x0.QueueAddTo(x0),
				x1.QueueAddTo(x1),
				y0.QueueAddTo(y0),
				SetNextPtr(vt, f_div_chain_init0[i - 1])
			]
		)
		
	f_div_chain_init2[0] << Trigger(
		nextptr = chain[0]
	)
	
	
	f_div_finalize1 << Trigger(
		nextptr = vt,
		actions = [
			# recover addresses of init1s
			[ SetNextPtr(f_div_chain_init1[i], f_div_chain_init2[i]) for i in range(32) ],
			a.QueueAssignTo(remainder),
			SetNextPtr(vt, f_div_finalize2)
		]
	)
	
	f_div_finalize2 << Trigger()
	
	
	
	
	
	# chain
	for i in range(32):
		cx0, cx1, cy0 = Forward(), Forward(), Forward()
		chain[i] << Trigger(
			conditions = [
				cx0 << a.AtLeast(0)
			],
			actions = [
				cx1 << a.SubtractNumber(0),
				cy0 << ret.AddNumber(0)
			]
		)
		
		chain_x0[i] << cx0 + 8
		chain_x1[i] << cx1 + 20
		chain_y0[i] << cy0 + 20
	
_initarith()

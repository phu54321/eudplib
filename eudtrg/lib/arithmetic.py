"""
Library for basic arithmetic operators

implements f_mul, f_div

"""

from eudtrg.base import * #@UnusedWildImport
from . import eudfunc, vtable

tok0 = PushTriggerScope()
vt = Addr(vtable.EUDVTable(7))
a, b, ret, remainder, x0, x1, y0 = vt.GetVariables()

# declaration for f_mul, f_div
# code from http://blog.naver.com/whyask37/140209918770
chain_x0 = [Addr() for _ in range(32)]
chain_x1 = [Addr() for _ in range(32)]
chain_y0 = [Addr() for _ in range(32)]
chain = [Addr() for _ in range(32)]


# f_mul
PushTriggerScope()

f_mul_chain_init0 = [Addr() for _ in range(32)]
f_mul_chain_init1 = [Addr() for _ in range(32)]
f_mul_begin = Addr()
f_mul_finalize = Addr()
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
			x0.QueueAssignTo(chain_x0[31 - i]),
			x1.QueueAssignTo(chain_x1[31 - i]),
			y0.QueueAssignTo(chain_y0[31 - i]),
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
	nextptr = vt,
	actions = [
		x0.QueueAddTo(x0),
		x1.QueueAddTo(x1),
		y0.QueueAddTo(y0),
		SetNextPtr(chain[31], f_mul_finalize),
		SetNextPtr(vt, chain[0])
	]
)

f_mul_finalize << Trigger()

PopTriggerScope()



# f_div impl
PushTriggerScope()

f_div_begin = Addr()
f_div_1 = Addr()
f_div_finalize1 = Addr()
f_div_finalize2 = Addr()
f_div_chain_init0 = [Addr() for _ in range(32)]
f_div_chain_init1 = [Addr() for _ in range(32)]
f_div_chain_init2 = [Addr() for _ in range(32)]

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
			x0.QueueAssignTo(chain_x0[i]),
			x1.QueueAssignTo(chain_x1[i]),
			y0.QueueAssignTo(chain_y0[i]),
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
		a.QueueAddTo(remainder),
		SetNextPtr(vt, f_div_finalize2)
	]
)

f_div_finalize2 << Trigger()

PopTriggerScope()


# chain

PushTriggerScope()
for i in range(31):
	cx0, cx1, cy0 = Addr(), Addr(), Addr()
	chain[i] << Trigger(
		conditions = [
			cx0 << Deaths(0, 0, 0, 0)
		],
		actions = [
			cx1 << SetDeaths(0, 0, 0, 0),
			cy0 << SetDeaths(0, 0, 0, 0)
		]
	)
	chain_x0 = cx0 + 8
	chain_x1 = cx1 + 20
	chain_x2 = cy0 + 20
PopTriggerScope()

PopTriggerScope(tok0)


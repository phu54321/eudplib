"""
Injector generator. This function injects payload into your map and some
initalization triggers into your map.
"""

import shutil
import struct

from ..maprw import mpqapi
from ..maprw import chktok

from .trigtrg import * #@UnusedWildImport
from ..dataspec.trigger import Trigger
from ..dataspec.forward import Forward
from ..stocktrg import SetDeaths
from ..payload.payload import CreatePayload

from ..utils.utils import EPD

def _CopyTrigger(player, conditions, iaddr, oaddrs, div4 = False):
	assert len(oaddrs) < 64

	triggers = []

	for i in range(31, 1, -1):
		triggers.append(CreateTRIGTrigger(
			players = [player],
			conditions = conditions + 
				[ CreateTRIGMemory(iaddr, AtLeast, 1<<i) ],
			actions = 
				[ CreateTRIGSetMemory(iaddr, Subtract, 1<<i) ] +
				[ CreateTRIGSetMemory(oaddr, Add, 1<<i if not div4 else 1<<(i-2)) for oaddr in oaddrs ] +
				[ CreateTRIGSetDeaths(player, Add, 1<<i, 37) ] # 37 from whyask37
		))

	for i in range(31, 1, -1):
		triggers.append(CreateTRIGTrigger(
			players = [player],
			conditions = conditions + 
				[ CreateTRIGDeaths(player, AtLeast, 1<<i, 37) ],
			actions = [
				CreateTRIGSetMemory(iaddr, Add, 1<<i),
				CreateTRIGSetDeaths(player, Subtract, 1<<i, 37)
			]
		))

	return triggers



def _AssignTrigger(player, conditions, value, oaddrs):
	assert len(oaddrs) < 64

	return CreateTRIGTrigger(
		players = [player],
		conditions = conditions,
		actions = [ CreateTRIGSetMemory(oaddr, SetTo, value) for oaddr in oaddrs ]
	)



def _file2eudtrg(player, conditions, fdata, offset):
	index = 0

	# create actions
	triggers = []
	actions = []
	while index < len(fdata):
		code = bytearray(fdata[index:index+4])
		index += 4

		if len(code) < 4:
			code[len(code):] = b'0' * (4 - len(code))

		number = struct.unpack('L', code)[0]
		actions.append(CreateTRIGSetMemory(offset, SetTo, number))
		offset += 4

	# pack actions to trigger
	index = 0
	while len(actions) > index:
		triggers.append(CreateTRIGTrigger(
			players = [player],
			conditions = conditions,
			actions = actions[index:index+64]
		))

		index += 64

	return triggers


"""
One button trigger injector.
 - input_map_path  : Map to use as skeleton
 - output_map_path : Map output path. Always replace duplicate items.
 - root			: First trigger to be executed.
"""
def Inject(input_map_path, output_map_path, root):
	# Read map
	mr = mpqapi.MpqRead()
	if not mr.Open(input_map_path):
		raise RuntimeError('[inject] Failed to open map \'%s\'.' % input_map_path)

	chk = mr.Extract('staredit\\scenario.chk')
	chkt = chktok.CHK()
	chkt.loadchk(chk)
	
	section_str = chkt.getsection('STR')
	section_mrgn = chkt.getsection('MRGN')
	
	payload_offset = -(-len(section_str) & ~0x3) + 4 # align by 4byte boundary and reserve 1 dword space for garbages.
	
	# We need to collect datas
	# - What player to execute trigger
	# - What player to execute 'vector'
	# - Size of previous STR section
	section_ownr = chkt.getsection('OWNR')
	pp = []
	cp = []

	# collect computer & player slot
	for i in range(12):
		if section_ownr[i] == 0x05:
			cp.append(i)
		elif section_ownr[i] == 0x06:
			pp.append(i)


	# Currently we only support maps with at least 2 human player.
	# TODO : This is not an intended behavior. Fix this so that EUDASM can be applied to any map.

	if len(cp) < 2:
		raise NotImplementedError('[Not implemented] Eudasm currently supports map with at least 2 computer players only.')
	
	
	injector = cp[0]
	executer = cp[1]
	
	
	# Add crash killer in front of the trigger
	triggerend = ~(0x51A284 + injector * 12)

	# For programs who missed putting triggerend to their last trigger.
	Trigger( nextptr = triggerend )
	
	entry = Forward()
	entry2 = Forward()
	
	entry << Trigger(
		nextptr = triggerend,
		actions = [
			SetDeaths(EPD(entry + 4), SetTo, entry2, 0)
		]
	)
	
	entry2 << Trigger(
		nextptr = root,
		actions = [
			SetDeaths(EPD(entry + 4), SetTo, triggerend, 0)
		]
	)
	
	payload = CreatePayload(entry)
	
	trgcode = payload.data
	ort = payload.orttable
	prt = payload.prttable
	
	# Injector plugins consists of 7 stages.
	#
	# Stage 1 : Create infinite loop			-> MRGN
	# Stage 2 : Initialize PRT Applier
	# Stage 3 : Run PRT Applier				 -> MRGN
	# Stage 4 : Initialize ORT Applier
	# Stage 5 : Run ORT Applier				 -> MRGN
	# Stage 6 : Delink infinite loop			-> MRGN
	# Stage 7 : Finalize, Jump to str section
	#

	triggers = []

	time = 0x0057F23C
	pts  = 0x0051A280
	mrgn = 0x0058DC60
	strs = 0x005993D4

	ptsinj = pts + 12 * injector
	ptsexc = pts + 12 * executer

	# Stage 1 : Create infinite loop
	#
	# (pts[injector]->prev)->next = mrgn
	#   *(mrgn + 328 + 16) = player(pts[injector]->prev + 4)
	#   *(mrgn + 328 + 20) = mrgn
	# *(mrgn + 328 + 24) = 0x072D0000
	#
	# (mrgn->next = *pts[injector]->next)
	#   *(mrgn + 4) = pts[injector]->next
	#
	# pts[executer]->next = mrgn
	#
	#   *(mrgn + 328 + 2048) = 4   for preserve trigger
	#
	
	# Trap trigger to be executed after a loop

	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Cleared),
			CreateTRIGDeaths(injector, Exactly, 1, 0)
		],
		actions = [
			CreateTRIGSetDeaths(injector, SetTo, 0, 0),
			CreateTRIGSetSwitch(0, SwitchSet)
		]
	))

	# Install trap, and set base things
	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Cleared)
		],
		actions = [
			CreateTRIGSetMemory(mrgn + 328 + 24, SetTo, 0x072D0000),		  # *(mrgn + 328 + 24) = 0x072D0000
			CreateTRIGSetMemory(ptsexc + 8, SetTo, mrgn),					 # pts[executer]->next = mrgn
			CreateTRIGSetMemory(mrgn + 328 + 16, SetTo, Memory2Player(4)),	#   *(mrgn + 328 + 16) = player(4)
			CreateTRIGSetMemory(mrgn + 328 + 20, SetTo, mrgn),				#   *(mrgn + 328 + 20) = mrgn
			CreateTRIGSetMemory(mrgn + 328 + 2048, SetTo, 4),				#   *(mrgn + 328 + 2048) = 4   for preserve trigger
			CreateTRIGSetDeaths(injector, SetTo, 1, 0) # Trap activator
		]
	))

	#   *(mrgn + 328 + 16) += (pts[injector]->prev) // 4
	triggers.extend(_CopyTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Cleared)
		],
		iaddr = ptsinj + 4,
		oaddrs = [mrgn + 328 + 16],
		div4 = True
	))

	#   *(mrgn + 4) = pts[injector]->next
	triggers.extend(_CopyTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Cleared)
		],
		iaddr = ptsinj + 8,
		oaddrs = [mrgn + 4],
	))



	# Variable for stage 3, 5
	addrcache = [0] * 32 # offset table

	# Stage 2-1 : Initialize Applier things
	#
	# Modify mrgn
	#  *(mrgn + 328 + 32 * i + 16) = Player(str + payload_offset)
	#  *(mrgn + 328 + 32 * i + 24) = 00 00 2D 08 = 0x082D0000

	
	#  *(mrgn + 328 + 32 * i + 16) = Player(payload_offset)
	triggers.append(_AssignTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Set),
			CreateTRIGSwitch(1, Cleared)
		],
		value = Memory2Player(payload_offset),
		oaddrs = [(mrgn + 328 + 32 * i + 16) for i in range(32)]
	))

	#  *(mrgn + 328 + 32 * i + 16) += str // 4
	triggers.extend(_CopyTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Set),
			CreateTRIGSwitch(1, Cleared)
		],
		iaddr = strs,
		oaddrs = [(mrgn + 328 + 32 * i + 16) for i in range(32)],
		div4 = True
	))



	#  *(mrgn + 328 + 32 * i + 24) = 00 00 2D 08 = 0x082D0000
	triggers.append(_AssignTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Set),
			CreateTRIGSwitch(1, Cleared)
		],
		value = 0x082D0000,
		oaddrs = [(mrgn + 328 + 32 * i + 24) for i in range(32)]
	))


	# Stage 2-2 : Initialize PRT Applier
	#
	#  *(mrgn + 328 + 32 * i + 20) = (str + payload_offset) // 4

	#  *(mrgn + 328 + 32 * i + 20) = payload_offset // 4
	triggers.append(_AssignTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Set),
			CreateTRIGSwitch(1, Cleared)
		],
		value = payload_offset // 4,
		oaddrs = [(mrgn + 328 + 32 * i + 20) for i in range(32)]
	))

	#  *(mrgn + 328 + 32 * i + 20) += str // 4
	triggers.extend(_CopyTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Set),
			CreateTRIGSwitch(1, Cleared)
		],
		iaddr = strs,
		oaddrs = [(mrgn + 328 + 32 * i + 20) for i in range(32)],
		div4 = True
	))


	# Jmp to next trigger (Stage 2)
	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(0, Set),
			CreateTRIGSwitch(1, Cleared)
		],
		actions = [
			CreateTRIGSetSwitch(1, SwitchSet)
		]
	))

	



	# Stage 3 : Run PRT Applier				 -> MRGN
	#  *(mrgn + 328 + 32 * i + 16) += offset
	loopn = (31 + len(prt)) // 32
	
	# Break condition
	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(1, Set),
			CreateTRIGSwitch(2, Cleared),
			CreateTRIGDeaths(injector, Exactly, loopn, 0)
		],
		actions = [
			CreateTRIGSetDeaths(injector, SetTo, 0, 0),
			CreateTRIGSetSwitch(2, SwitchSet)
		]
	))

	# Filling
	for i in range(loopn):
		startindex = i * 32
		subprt = prt[startindex:startindex+32]
		if len(subprt) < 32:
			subprt += [-4] * (32 - len(subprt))

		poffset = [(subprt[i] - addrcache[i]) // 4 for i in range(32)]
		addrcache = subprt

		triggers.append(CreateTRIGTrigger(
			players = [injector],
			conditions = [
				CreateTRIGMemory(time, Exactly, 2),
				CreateTRIGSwitch(1, Set),
				CreateTRIGSwitch(2, Cleared),
				CreateTRIGDeaths(injector, Exactly, i, 0)
			],
			actions = [ CreateTRIGSetMemory(mrgn + 328 + 32 * j + 16, Add, poffset[j]) for j in range(32) ]
		))

	# Advancer
	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(1, Set),
			CreateTRIGSwitch(2, Cleared)
		],
		actions = [
			CreateTRIGSetDeaths(injector, Add, 1, 0),
			CreateTRIGPreserveTrigger()
		]
	))
	




	# Stage 4 : Initialize ORT Applier
	#
	#  *(mrgn + 328 + 32 * i + 20) = str + payload_offset

	#  *(mrgn + 328 + 32 * i + 20) = payload_offset
	triggers.append(_AssignTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(2, Set),
			CreateTRIGSwitch(3, Cleared)
		],
		value = payload_offset,
		oaddrs = [(mrgn + 328 + 32 * i + 20) for i in range(32)]
	))

	#  *(mrgn + 328 + 32 * i + 20) += str
	triggers.extend(_CopyTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(2, Set),
			CreateTRIGSwitch(3, Cleared)
		],
		iaddr = strs,
		oaddrs = [(mrgn + 328 + 32 * i + 20) for i in range(32)],
	))

	# Jmp to next stage
	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(2, Set),
			CreateTRIGSwitch(3, Cleared)
		],
		actions = [
			CreateTRIGSetSwitch(3, SwitchSet)
		]
	))





	# Stage 5 : Run ORT Applier				 -> MRGN
	#  *(mrgn + 328 + 32 * i + 16) += offset
	loopn = (31 + len(ort)) // 32
	
	# Break condition
	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(3, Set),
			CreateTRIGSwitch(4, Cleared),
			CreateTRIGDeaths(injector, Exactly, loopn, 0)
		],
		actions = [
			CreateTRIGSetDeaths(injector, SetTo, 0, 0),
			CreateTRIGSetSwitch(4, SwitchSet)
		]
	))

	# Filling
	for i in range(loopn):
		startindex = i * 32
		subort = ort[startindex:startindex+32]
		if len(subort) < 32:
			subort += [-4] * (32 - len(subort))

		poffset = [(subort[j] - addrcache[j]) // 4 for j in range(32)]
		addrcache = subort

		triggers.append(CreateTRIGTrigger(
			players = [injector],
			conditions = [
				CreateTRIGMemory(time, Exactly, 2),
				CreateTRIGSwitch(3, Set),
				CreateTRIGSwitch(4, Cleared),
				CreateTRIGDeaths(injector, Exactly, i, 0)
			],
			actions = [ CreateTRIGSetMemory(mrgn + 328 + 32 * j + 16, Add, poffset[j]) for j in range(32) ]
		))

	# Advancer
	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(3, Set),
			CreateTRIGSwitch(4, Cleared)
		],
		actions = [
			CreateTRIGSetDeaths(injector, Add, 1, 0),
			CreateTRIGPreserveTrigger()
		]
	))

	# Stage 6 : Delink infinite loop			-> MRGN
	#
	# *(mrgn + 328 + 16) = player(pts[injector]->prev + 4)
	# *(mrgn + 328 + 20) = str + payload_offset
	# *(mrgn + 328 + 24) = 0x072D0000
	# *(mrgn + 328 + 32 + 24) = 0x00000000
	#

	# Exit trap
	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(4, Set),
			CreateTRIGSwitch(5, Cleared),
			CreateTRIGDeaths(injector, Exactly, 1, 0)
		],
		actions = [
			CreateTRIGSetDeaths(injector, SetTo, 0, 0),
			CreateTRIGSetSwitch(5, SwitchSet)
		]
	))

	# *(mrgn + 328 + 16) = player(4)
	# *(mrgn + 328 + 20) = payload_offset
	# *(mrgn + 328 + 24) = 0x072D0000
	# *(mrgn + 328 + 32 + 24) = 0x00000000

	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(4, Set),
			CreateTRIGSwitch(5, Cleared)
		],
		actions = [
			CreateTRIGSetMemory(mrgn + 328 + 16, SetTo, Memory2Player(4)),
			CreateTRIGSetMemory(mrgn + 328 + 20, SetTo, payload_offset),
			CreateTRIGSetMemory(mrgn + 328 + 24, SetTo, 0x072D0000),
			CreateTRIGSetMemory(mrgn + 328 + 32 + 24, SetTo, 0x00000000),
			CreateTRIGSetDeaths(injector, SetTo, 1, 0), # activates trap
		]
	))

	#   *(mrgn + 328 + 16) += (pts[injector]->prev) // 4
	triggers.extend(_CopyTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(4, Set),
			CreateTRIGSwitch(5, Cleared)
		],
		iaddr = ptsinj + 4,
		oaddrs = [mrgn + 328 + 16],
		div4 = True
	))

	#   *(mrgn + 328 + 20) += (strs) // 4
	triggers.extend(_CopyTrigger(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(4, Set),
			CreateTRIGSwitch(5, Cleared)
		],
		iaddr = strs,
		oaddrs = [mrgn + 328 + 20]
	))

	# Stage 7 : Finalize, Jump to str section
	#
	# pts[executer]->prev = ptsexc+4
	# pts[executer]->next = ~(ptsexc+4)
	# 
	# Restore MRGN data
	#


	triggers.extend(_file2eudtrg(
		player = injector,
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(5, Set)
		],
		fdata = section_mrgn,
		offset = mrgn
	))

	triggers.append(CreateTRIGTrigger(
		players = [injector],
		conditions = [
			CreateTRIGMemory(time, Exactly, 2),
			CreateTRIGSwitch(5, Set)
		],
		actions = [
			CreateTRIGSetSwitch(0, SwitchClear),
			CreateTRIGSetSwitch(1, SwitchClear),
			CreateTRIGSetSwitch(2, SwitchClear),
			CreateTRIGSetSwitch(3, SwitchClear),
			CreateTRIGSetSwitch(4, SwitchClear),
			CreateTRIGSetSwitch(5, SwitchClear),
			CreateTRIGSetMemory(ptsexc + 4, SetTo, ptsexc+4),
			CreateTRIGSetMemory(ptsexc + 8, SetTo, ~(ptsexc+4)),
		]
	))


	# All stages written.
	trig = b''.join([bytes(t) for t in triggers])
	chkt.setsection('TRIG', trig)

	# Append trig to STR section
	section_str = section_str + bytes([0] * (payload_offset - len(section_str))) + trgcode
	chkt.setsection('STR ', section_str)

	# Set mrgn to blank one.
	chkt.setsection('MRGN', b'\x00' * 5100)
	chkt.optimize()
	
	chk = chkt.savechk()

	# Write to file
	try:
		shutil.copyfile(input_map_path, output_map_path)
	except OSError:
		raise RuntimeError('Copyfile from \'%s\' to \'%s\' failed.' % (input_map_path, output_map_path))
	
	mw = mpqapi.MpqWrite()
	if not mw.Open(output_map_path, preserve_content = True):
		raise RuntimeError('Cannot open output file \'%s\'.' % output_map_path)
	

	mw.PutFile('staredit\\scenario.chk', chk)
	mw.Compact()
	mw.Close()
	
	print('Injection Complete')

	return True

from eudtrg import *

'''
Creep reading
'''

def CreateCreepReadFunc():
	global f_creepread_init, f_creepread

	creepvt = EUDVTable(9)
	x, y, ret, creepaddr, mapwidth, mapheight, creepindex, creeptileaddr, creepevenodd = creepvt.GetVariables()


	# f_creepread_init
	creepread_init_begin = Forward()
	creepread_init_end = Forward()
	f_creepread_init = EUDFunc(creepread_init_begin, creepread_init_end, creepvt, 0, 0)

	creepread_init_begin << NextTrigger()

	# Get creepmap address
	ret_creepaddr = f_dwread.call(EPD(0x6D0E84))
	ret_creepaddr = f_epd.call(ret_creepaddr) # convert to epd player
	VTProc(f_epd.GetVTable(), [
		ret_creepaddr.QueueAssignTo(creepaddr)
	])


	# Get map width & height
	ret_mapwh = f_dwread.call(EPD(0x57F1D4))
	ret_mapw, ret_maph = f_dwbreak.call(ret_mapwh)[0:2]
	VTProc(f_dwbreak.GetVTable(), [
		ret_mapw.QueueAssignTo(mapwidth),
		ret_maph.QueueAssignTo(mapheight)
	])

	creepread_init_end << Trigger()





	# f_creepread
	creepread_begin = Forward()
	creepread_end = Forward()
	f_creepread = EUDFunc(creepread_begin, creepread_end, creepvt, 2, 1)

	creepread_begin << NextTrigger()

	# calculate creepindex = y * mapwidth + x
	ret_m = f_mul.call(y, mapwidth)
	VTProc(f_mul.GetVTable(), [
		creepindex.SetNumber(0),
		ret_m.QueueAddTo(creepindex)
	])

	VTProc(creepvt, [
		x.QueueAddTo(creepindex)
	])

	# ok. Divide this by 2.
	ret_addrindex, ret_selector = f_div.call(creepindex, 2)
	VTProc(f_div.GetVTable(), [
		ret_addrindex.QueueAssignTo(creeptileaddr), # This will be our tile address
		ret_selector.QueueAssignTo(creepevenodd)
	])

	VTProc(creepvt, [ creepaddr.QueueAddTo(creeptileaddr) ])

	# read tile data
	ret_creeptiledata = f_dwread.call(creeptileaddr)

	ret_creeptiledata_word0, ret_creeptiledata_word1 = f_dwbreak.call(ret_creeptiledata)[0:2]
	

	# select word0/word1 by evenodd
	creepbr0 = Forward()
	creepbr1 = Forward()
	creepbrend = Forward()
	EUDIf( [creepevenodd.Exactly(0)], creepbr0, creepbr1 )

	# even
	creepbr0 << NextTrigger()
	VTProc(f_dwbreak.GetVTable(), [
		ret_creeptiledata_word0.QueueAssignTo(ret)
	])
	Trigger( nextptr = creepbrend )

	# odd
	creepbr1 << NextTrigger()
	VTProc(f_dwbreak.GetVTable(), [
		ret_creeptiledata_word1.QueueAssignTo(ret)
	])

	creepbrend << NextTrigger()

	creepread_end << Trigger()

CreateCreepReadFunc()




# Iterate through each units.
vt = EUDVTable(7)
unitptr, unitepd, tmpepd, unitx, unity, tileunitx, tileunity = vt.GetVariables()


start = Trigger()
f_creepread_init.call()
start1 = Forward()
start1 << Trigger(
	actions = [
		SetNextPtr(start, start1)
	]
)


# Turbo trigger
Trigger(
	actions = [
		SetDeaths(203151, SetTo, 1, 0), # turbo trigger
	]
)


ret_unit = f_dwread.call(EPD(0x628430))
VTProc(f_dwread.GetVTable(), [
	ret_unit.QueueAssignTo(unitptr)
])


# loop start

loopout = Forward()
loopstart = NextTrigger()
loopcontinue = Forward()



if 1:
	EUDJumpIf( [unitptr.Exactly(0)], loopout ) # traversed all units -> break

	# Convert addr -> epd
	ret_unitepd = f_epd.call(unitptr)
	VTProc(f_epd.GetVTable(), [
		ret_unitepd.QueueAssignTo(unitepd)
	])


	# Get unit type
	# +0x0064   uint16 unittype
	VTProc(vt, [
		tmpepd.SetNumber(0x64 // 4),
		unitepd.QueueAddTo(tmpepd)
	])

	ret_v = f_dwread.call(tmpepd)
	ret_ut = f_dwbreak.call(ret_v)[0]

	EUDJumpIfNot( [ret_ut.Exactly(37)], loopcontinue ) # not zergling -> continue

	# This unit is zergling.

	
	# Get x, y coordinates of this unit.
	VTProc(vt, [
		tmpepd.SetNumber(0x28 // 4),
		unitepd.QueueAddTo(tmpepd)
	])

	ret_xy = f_dwread.call(tmpepd)
	ret_x, ret_y = f_dwbreak.call(ret_xy)[0:2]
	VTProc(f_dwbreak.GetVTable(), [
		ret_x.QueueAssignTo(unitx),
		ret_y.QueueAssignTo(unity)
	])

	
	# Convert coordinates to tile coord
	ret_tilex = f_div.call(unitx, 32)[0]
	VTProc(f_div.GetVTable(), [ ret_tilex.QueueAssignTo(tileunitx) ])
	ret_tiley = f_div.call(unity, 32)[0]
	VTProc(f_div.GetVTable(), [ ret_tiley.QueueAssignTo(tileunity) ])

	ret_creepval = f_creepread.call(tileunitx, tileunity)

	# If there is no creep, then continue
	EUDJumpIf( [
		ret_creepval.AtLeast(16),
		ret_creepval.AtMost(31)
	], loopcontinue ) # not zergling -> continue


	# There is a creep. Now let's create radiation.
	# Set first location's coordinates to (x,y) - (x,y)
	VTProc(vt, [
		unitx.QueueAssignTo(EPD(0x0058DC60 + 0)),
		unity.QueueAssignTo(EPD(0x0058DC60 + 4)),
	])
	
	VTProc(vt, [
		unitx.QueueAssignTo(EPD(0x0058DC60 + 8)),
		unity.QueueAssignTo(EPD(0x0058DC60 + 12)),
	])
	
	# Create kakaru there
	Trigger(
		actions = [
			CreateUnit(1, DefUnitID['Kakaru (Twilight Critter)'], 1, Player1)
		]
	)


	# Loop done. Get next unit pointer
	loopcontinue << NextTrigger()

	VTProc(vt, [
		tmpepd.SetNumber(1),
		unitepd.QueueAddTo(tmpepd)
	])

	ret_next = f_dwread.call(tmpepd)
	VTProc(f_dwread.GetVTable(), [
		ret_next.QueueAssignTo(unitptr)
	])

	Trigger( nextptr = loopstart )



loopout << NextTrigger()


Trigger(
	nextptr = triggerend,
	actions = [
		RemoveUnit( DefUnitID['Kakaru (Twilight Critter)'], Player1 ),
	]
)



Inject('outputmap/creeptest_basemap.scx', 'outputmap/creeptest.scx', start)
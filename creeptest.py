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
	SetVariables(creepaddr, f_epd.call(f_dwread.call(EPD(0x6D0E84)))) # Get creepmap address
	SetVariables( [mapwidth, mapheight], f_dwbreak.call(f_dwread.call(EPD(0x57F1D4)))[0:2] ) # Get map width & height
	creepread_init_end << Trigger()


	# f_creepread
	creepread_begin = Forward()
	creepread_end = Forward()
	f_creepread = EUDFunc(creepread_begin, creepread_end, creepvt, 2, 1)

	creepread_begin << NextTrigger()

	
	# calculate creepindex = y * mapwidth + x
	SetVariables(creepindex, f_mul.call(y, mapwidth))
	SetVariables(creepindex, x, Add)
	# creeptileaddr = creepindex // 2, creepevenodd = creepindex % 2
	SetVariables( [creeptileaddr, creepevenodd], f_div.call(creepindex, 2) )
	# creeptileaddr += creepaddr
	SetVariables(creeptileaddr, creepaddr, Add)

	# read tile data
	ret_creeptiledata = f_dwread.call(creeptileaddr)
	ret_creeptiledata_word0, ret_creeptiledata_word1 = f_dwbreak.call(ret_creeptiledata)[0:2]
	

	# select word0/word1 by evenodd
	creepbr0, creepbr1, creepbrend = Forward(), Forward(), Forward()
	EUDIf( [creepevenodd.Exactly(0)], creepbr0, creepbr1 )

	# on even
	creepbr0 << NextTrigger()
	SetVariables(ret, ret_creeptiledata_word0)
	EUDJump(creepbrend)

	# on odd
	creepbr1 << NextTrigger()
	SetVariables(ret, ret_creeptiledata_word1)

	# end
	creepbrend << NextTrigger()
	creepread_end << Trigger()

CreateCreepReadFunc()



'''
Main logic
'''


start = Trigger()
f_creepread_init.call()
start1 = Forward()
start1 << Trigger(
	actions = [
		SetNextPtr(start, start1)
	]
)


# Turbo trigger
DoActions(SetDeaths(203151, SetTo, 1, 0))

# Iterate through each units.
vt = EUDVTable(7)
unitptr, unitepd, tmpepd, unitx, unity, tileunitx, tileunity = vt.GetVariables()

SetVariables(unitptr, f_dwread.call(EPD(0x628430)))

# loop start
loopout = Forward()
loopstart = NextTrigger()
loopcontinue = Forward()


if 1:
	EUDJumpIf( [unitptr.Exactly(0)], loopout ) # traversed all units -> break

	# Convert addr -> epd
	SetVariables(unitepd, f_epd.call(unitptr))

	# Get unit type
	# +0x0064   uint16 unittype
	VTProc(vt, [
		tmpepd.SetNumber(0x64 // 4),
		unitepd.QueueAddTo(tmpepd)
	])

	# Continue if the unit is not zergling
	ret_ut = f_dwbreak.call(f_dwread.call(tmpepd))[0]
	EUDJumpIfNot( [ret_ut.Exactly(37)], loopcontinue ) # not zergling -> continue

	
	# Get x, y coordinates of this unit.
	VTProc(vt, [
		tmpepd.SetNumber(0x28 // 4),
		unitepd.QueueAddTo(tmpepd)
	])

	SetVariables([unitx, unity], f_dwbreak.call(f_dwread.call(tmpepd))[0:2])

	
	# Convert coordinates to tile coord
	SetVariables(tileunitx, f_div.call(unitx, 32)[0])
	SetVariables(tileunity, f_div.call(unity, 32)[0])

	# If there is no creep, then continue
	ret_creepval = f_creepread.call(tileunitx, tileunity) # read creep value
	EUDJumpIf( [
		ret_creepval.AtLeast(16),
		ret_creepval.AtMost(31)
	], loopcontinue ) # not zergling -> continue


	# Slow down zergling.
	# Creating kakaru and killing them slows down zergling.
	SetVariables(
		[
			EPD(0x0058DC60 + 0),
			EPD(0x0058DC60 + 4),
		], [unitx, unity]
	)

	SetVariables(
		[
			EPD(0x0058DC60 + 8),
			EPD(0x0058DC60 + 12)
		], [ unitx, unity ]
	)

	DoActions(CreateUnit(1, DefUnitID['Kakaru (Twilight Critter)'], 1, Player1))

	# Loop done. Get next unit pointer
	loopcontinue << NextTrigger()

	VTProc(vt, [
		tmpepd.SetNumber(1),
		unitepd.QueueAddTo(tmpepd)
	])

	SetVariables(unitptr, f_dwread.call(tmpepd))

	Trigger( nextptr = loopstart )



loopout << NextTrigger()


Trigger(
	nextptr = triggerend,
	actions = [
		RemoveUnit( DefUnitID['Kakaru (Twilight Critter)'], Player1 ),
	]
)



Inject('outputmap/creeptest_basemap.scx', 'outputmap/creeptest.scx', start)

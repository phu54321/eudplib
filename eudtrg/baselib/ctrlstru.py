from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport

def DoActions(actions):
    Trigger( actions = FlattenList(actions) )

def EUDJump(nexttrg):
<<<<<<< HEAD
	Trigger( nextptr = nexttrg )

def EUDBranch(conditions, ontrue, onfalse):
	brtrg = Forward()
	ontruetrg = Forward()
	
	brtrg << Trigger(
		nextptr = onfalse,
		conditions = conditions,
		actions = [
			SetNextPtr(brtrg, ontruetrg)
		]
	)
	
	ontruetrg << Trigger(
		nextptr = ontrue,
		actions = [
			SetNextPtr(brtrg, onfalse)
		]
	)
	
=======
    Trigger( nextptr = nexttrg )

def EUDBranch(conditions, ontrue, onfalse):
    brtrg = Forward()
    ontruetrg = Forward()

    brtrg << Trigger(
        nextptr = onfalse,
        conditions = conditions,
        actions = [
            SetNextPtr(brtrg, ontruetrg)
        ]
    )

    ontruetrg << Trigger(
        nextptr = ontrue,
        actions = [
            SetNextPtr(brtrg, onfalse)
        ]
    )

>>>>>>> development
def EUDJumpIf(conditions, ontrue):
    brtrg = Forward()
    ontruetrg = Forward()
    onfalse = Forward()

    brtrg << Trigger(
        nextptr = onfalse,
        conditions = conditions,
        actions = [
            SetNextPtr(brtrg, ontruetrg)
        ]
    )

    ontruetrg << Trigger(
        nextptr = ontrue,
        actions = [
            SetNextPtr(brtrg, onfalse)
        ]
    )

    onfalse << NextTrigger()


def EUDJumpIfNot(conditions, onfalse):
<<<<<<< HEAD
	brtrg = Forward()
	ontrue = Forward()
	
	brtrg << Trigger(
		nextptr = onfalse,
		conditions = conditions,
		actions = [
			SetNextPtr(brtrg, ontrue)
		]
	)
	
	ontrue << Trigger(
		actions = [
			SetNextPtr(brtrg, onfalse)
		]
	)
	
=======
    brtrg = Forward()
    ontrue = Forward()

    brtrg << Trigger(
        nextptr = onfalse,
        conditions = conditions,
        actions = [
            SetNextPtr(brtrg, ontrue)
        ]
    )

    ontrue << Trigger(
        actions = [
            SetNextPtr(brtrg, onfalse)
        ]
    )



def EUDWhile(conditions, block_start, block_end):
    out = Forward()

    forstart = NextTrigger()
    EUDJumpIf(conditions, block_start, out)
    block_end.MUTATE_SetNextPtr(forstart)

    out << NextTrigger()

>>>>>>> development

from ..base import *

def EUDIf(conditions, ontrue, onfalse):
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
	
	onfalse = NextTrigger()
	
	
def EUDJumpIfNot(conditions, onfalse):
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
	block_end.MUTATE_SetNextPtr(forstart)
	EUDJumpIfNot(conditions, out)
	
	out << NextTrigger()
	
METHOD TurnOn : BOOL
VAR_INPUT
	MotorI:MotorI;
END_VAR
VAR_OUTPUT
	MotorO:MotorO;
END_VAR
VAR
	WaitTimer:TON;
	InternalSequenceDelay:time;
END_VAR

IF MotorO.FaultStatus = FALSE THEN
	WaitTimer(IN:=TRUE , PT:=InternalSequenceDelay);
END_IF

IF WaitTimer.Q THEN
	MotorO.Coil:=TRUE;
	WaitTimer(IN:=FALSE);
END_IF
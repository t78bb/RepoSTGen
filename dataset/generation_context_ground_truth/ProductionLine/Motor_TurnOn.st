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
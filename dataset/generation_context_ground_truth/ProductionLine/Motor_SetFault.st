VAR
	WaitTimer:TON;
	InternalSequenceDelay:time;
END_VAR

IF MotorI.Overload THEN
	MotorO.FaultStatus:=TRUE;
	TurnOff();
END_IF
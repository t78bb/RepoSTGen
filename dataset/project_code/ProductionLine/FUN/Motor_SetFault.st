METHOD SetFault : BOOL
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

IF MotorI.Overload THEN
	MotorO.FaultStatus:=TRUE;
	TurnOff();
END_IF
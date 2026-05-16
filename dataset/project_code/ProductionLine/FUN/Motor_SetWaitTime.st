METHOD SetWaitTime : BOOL
VAR_INPUT
	MotorI:MotorI;
	SequenceDelay:TIME;
END_VAR
VAR_OUTPUT
	MotorO:MotorO;
END_VAR
VAR
	WaitTimer:TON;
	InternalSequenceDelay:time;
END_VAR

InternalSequenceDelay:=SequenceDelay;
FUNCTION_BLOCK Motor
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


SetFault();
ResetFault();
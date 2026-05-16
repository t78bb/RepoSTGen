VAR
	WaitTimer:TON;
	InternalSequenceDelay:time;
	ResetDetect:r_trig;
END_VAR

ResetDetect(CLK:=MotorI.FaultReset);

IF ResetDetect.Q THEN
	MotorO.FaultStatus:=FALSE;
END_IF
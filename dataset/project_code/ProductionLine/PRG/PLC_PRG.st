PROGRAM PLC_PRG
VAR
	Motor:Motor;
	MotorInputs:MotorI;
	MotorOutputs:MotorO;
	liga: BOOL;
	desliga: BOOL;
	settime: BOOL;
	setfault: BOOL;
	reset: BOOL;
	timetemp: TIME;
END_VAR

Motor(MotorI:=MotorInputs , MotorO=>MotorOutputs );

IF liga THEN
	Motor.TurnOn();
	liga:=FALSE;
END_IF

IF desliga THEN
	Motor.TurnOff();
	desliga:=FALSE;
END_IF

IF settime THEN
	motor.SetWaitTime(SequenceDelay:=timetemp);
	settime:=FALSE;
END_IF

IF setfault THEN
	motor.SetFault();
	setfault:=FALSE;
END_IF

IF reset THEN
	motor.ResetFault();
	reset:=FALSE;
END_IF
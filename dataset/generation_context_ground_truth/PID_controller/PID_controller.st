VAR CONSTANT
	millis: UINT := 1000;
END_VAR
VAR
	now: TIME := T#0S;
	lastTime: TIME := T#0S;
	err: REAL := 0; //Process error
	lastCO_P: REAL := 0;  //Used for calculation of the derivative term
	delta_t: REAL;
	lastPV: REAL := 0;
END_VAR

//Check parameters
//Ti division by zero
IF Ti = 0 THEN
	Ti := 1;
END_IF

//Update PID parameters every sampleTime
now := TIME();
IF ((now - lastTime) > SampleTime) THEN
	err := SP - PV;
	delta_t := TIME_TO_REAL(SampleTime)/millis;
	CO_P := Kc * err;
	CO_I := CO_I + 1/Ti * CO_P * delta_t;
	//Add wind-up for CO_I
	IF CO_I < LowerLimit THEN
		CO_I := LowerLimit;
	ELSIF CO_I > UpperLimit THEN
		CO_I := UpperLimit;
	END_IF;
	
	//Observe that d(err)/dt = d(SP)/dt - d(PV)/dt
	//If SP constant,
	//d(err)/dt = - d(PV)/dt
	//Good: no output spikes
	//Bad: some processes need more aggressive tuning
	IF delta_t <> 0 THEN
		CO_D := Td * (PV - lastPV)/delta_t;
	END_IF;
	
	//A different approch would be with a tunable filter
	
	CO := CO_P + CO_I + CO_D;
	//Add wind-up for CO
	IF CO < LowerLimit THEN
		CO := LowerLimit;
	ELSIF CO > UpperLimit THEN
		CO := UpperLimit;
	END_IF;
	
	lastTime := now;
	lastPV := PV;
END_IF;
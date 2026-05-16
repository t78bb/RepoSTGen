VAR
	now: TIME;
	lastTime: TIME;
	lastPV:REAL := 140;
	A: REAL;
	B: REAL;
	delta_t: REAL;
END_VAR
VAR CONSTANT
	millis: REAL := 1000;
END_VAR

now := TIME();
IF ((now - lastTime) > Sample_time) THEN
	delta_t := TIME_TO_REAL(Sample_time)/millis;
	A := EXP(-delta_t/Tp);
	B := 1 - A;
	C := 2;
	
	//PV := A * lastPV + B * Kp * CO + C;
	PV := 0.987 * lastPV - 0.00679 * CO + C;
	lastPV := PV;

	lastTime := now;
END_IF 
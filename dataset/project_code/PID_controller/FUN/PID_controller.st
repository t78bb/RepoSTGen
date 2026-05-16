//***************************************************************
//* A simple PID controller for Codesys.
//* by Alexander Jaworowski
//* Inspiration from https://github.com/br3ttb/Arduino-PID-Library
//* https://github.com/alexjaw/PID_controller
//* This Library is licensed under a MIT License
//
// 2015-02-22	Bug fix in the calculation of CO_I.
//				Added derivative term (d(err)/dt = -d(PV)/dt, i.e.
//				derivative on measurements
//***************************************************************
FUNCTION_BLOCK PID_controller
VAR_INPUT
	SP : REAL;
	PV : REAL;
	Kc : REAL;
	Ti : REAL;
	Td : REAL;
	SampleTime: TIME; //Should be ~0.1 * Tp, Tp : the process time [http://www.controlguru.com/2007/012807.html]
	LowerLimit: REAL;
	UpperLimit: REAL;
END_VAR
VAR_OUTPUT
	CO: REAL; //Controller Output
	CO_P: REAL; //Prportional term
	CO_I: REAL; //Integral term
	CO_D: REAL; //Derivative term
END_VAR
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
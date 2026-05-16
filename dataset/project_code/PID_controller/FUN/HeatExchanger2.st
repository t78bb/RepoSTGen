// AJ Jaworowski 2015-02-23
// Following the presentation on
// http://openenergymonitor.org/emon/node/2999
FUNCTION_BLOCK HeatExchanger2
VAR_INPUT
	Heat_In:		REAL;		//In principle a radiator in the room [W]
	U:				REAL;		//Thermal conductance [W/K]
	TC:				REAL;		//Thermal capacity [J/K], commonly cv, specific heat capacity [J/kgK]
								//we use a smaller value than in reality, so that we can see changes
								//during a life-time...
	Temp_In:		REAL;		//Start temperature in the room [K]
	Temp_Out:		REAL;		//Outside temperature [K] 
	Sample_time:	TIME;
END_VAR
VAR_OUTPUT
	Temp:			REAL;		//The resulting room temperature
END_VAR
VAR
	now: TIME;
	lastTime: TIME := T#0s;
	delta_t: REAL;
	heat_flow: REAL;
	lastTemp: REAL;
END_VAR
VAR CONSTANT
	millis: REAL := 1000;
END_VAR

now := TIME();
IF ((now - lastTime) > Sample_time) THEN
	delta_t := TIME_TO_REAL(Sample_time)/millis;
	
	//First calculate net heat
	//Heat_In is our heat source
	//Second term is heat flow depending on temperature difference
	//Obs: At start, set lastTime to start temp Temp_In
	IF lastTime = T#0S THEN
		lastTemp := Temp_In;
	END_IF
	heat_flow := Heat_In - U * (lastTemp - Temp_Out);
	
	//Second: calculate temperature change due to heat_flow
	Temp := lastTemp + heat_flow * delta_t / TC;
	
	//Update variables for next iteration
	lastTemp := Temp;
	lastTime := now;
END_IF;
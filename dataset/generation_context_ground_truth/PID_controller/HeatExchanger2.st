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
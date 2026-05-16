//A.J. Jaworowski 2015-02-20
//Simulering av en tank med RedBull
FUNCTION_BLOCK Tank
VAR_INPUT
	Process_In: REAL;  //Flöde in per sekund, testa vad som händer on du matar in 100
					   //Därefter ska regulatorns OUT in i denna ingång.
	Process_Out: REAL; //Flöde ut per sekund, typ 90
					   //Effekten blir att tanken fylls med 10 per sekund
					   //Full efter ca 1 minut - testa
	SampleTime: TIME;  //Uppdateringstid, typ 100ms
	Lower_limit: REAL; //Tankens lägsta nivå, typ 0
	Upper_limit: REAL; //Tankens max nivå, kanske 500
END_VAR
VAR_OUTPUT
	Level: REAL; //Nivån i tanken
END_VAR
VAR
	now: TIME;
	lastTime: TIME;
	proc_sum_in: REAL := 0;
	proc_sum_out: REAL := 0;
	temp: REAL;
	millis: UINT := 1000;
	proc_out: REAL;
END_VAR

now := TIME();
IF ((now - lastTime) > SampleTime) THEN
	Level := Level +  TIME_TO_REAL(SampleTime)/millis * (Process_In - Process_Out);
	IF Level < Lower_limit THEN
		Level := Lower_limit;
	ELSIF Level > Upper_limit THEN
		Level := Upper_limit;
	END_IF;
	lastTime := now;
END_IF;
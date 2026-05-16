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
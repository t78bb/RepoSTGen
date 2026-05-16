FUNCTION_BLOCK FB_角速度转线速度
VAR_INPUT
	Enble: BOOL;
	角速度: REAL;
	直径: REAL; // mm
	减速比: REAL;
END_VAR
VAR_OUTPUT	
	线速度: REAL; // m/min
END_VAR
VAR
END_VAR

IF Enble THEN 
	线速度:=LREAL_TO_REAL(角速度*(60.0*3.14159265358979*(直径/2.0))/(1000.0*180.0))/减速比;
END_IF;
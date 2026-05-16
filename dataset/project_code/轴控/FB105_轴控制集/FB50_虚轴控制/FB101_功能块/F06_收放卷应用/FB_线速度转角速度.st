FUNCTION_BLOCK FB_线速度转角速度
VAR_INPUT
	Enble: BOOL;
	线速度: REAL; // m/min
	直径: REAL; // mm
	减速比: REAL;
END_VAR
VAR_OUTPUT
	角速度: REAL;
END_VAR
VAR
END_VAR

IF Enble THEN 
	角速度:=1000.0*线速度*180.0/(60.0*3.14159265358979*((直径/1000.00)/2.0))*减速比;
END_IF;
// 1弧度=180°/π    弧角速度=V/R    角速度（°）=V/R*180°/π
FUNCTION Fun_模拟量比例换算 : INT
VAR_INPUT
rOutput: REAL; (* [] Physical output *)
rPhyMin: REAL; (* [] Physical minimum *)
rPhyMax: REAL; (* [] Physical maximum *)
eTerminal: E_Ctrl_TerminalType; (* [] Terminal type. *)
END_VAR
VAR
rTerMin: REAL;
rTerMax: REAL;
rPhyRange: REAL;
rTerRange: REAL;
rTerOutput: REAL;
END_VAR

rTerMax:= 32768.0;

CASE eTerminal OF
eTerminal_0mA_20mA: rTerMin:= 0.0;
eTerminal_4mA_20mA: rTerMin:= 0.0;
eTerminal_0V_10V: rTerMin:= 0.0;
eTerminal_m10V_10V: rTerMin:= -32768.0;
ELSE
rTerMin:= -32768.0;
END_CASE

rPhyRange:= rPhyMax - rPhyMin;
rTerRange:= rTerMax - rTerMin;

IF rPhyRange > 0.0 AND rTerRange > 0.0 THEN
	rTerOutput:= rTerMin + (rTerRange * (rOutput - rPhyMin) / rPhyRange);
ELSE
    rTerOutput:= 0.0;
END_IF


Fun_模拟量比例换算:= REAL_TO_INT(rTerOutput);

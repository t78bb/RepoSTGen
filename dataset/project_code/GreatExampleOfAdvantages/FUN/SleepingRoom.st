FUNCTION_BLOCK SleepingRoom
VAR_INPUT
END_VAR
VAR_OUTPUT
END_VAR
VAR
	Lamp1:LampBase;		
	
	ligthButton1: BOOL;
	
	Lamp1Out: BOOL;
	
	Temperature:TemperatureBase;
	
	//gernerates a sin as temperature
	Temp:OSCAT_BASIC.GEN_SIN;
END_VAR

Lamp1(SwitchIn:= ligthButton1, LampOut=> Lamp1Out);

Temp(
	PT:= T#60S, 
	AM:= 1.5, 
	OS:= 15.0, 
	DL:= 0.0);
	
	
Temperature(tempIn:= Temp.Out);
FUNCTION_BLOCK MainBath
VAR_INPUT
END_VAR
VAR_OUTPUT
END_VAR
VAR
	Lamp1:LampBase;
	Lamp2:LampBase;
	Lamp3:LampBase;
	
	Temperature:TemperatureBase;
	
	
	ligthButton1: BOOL;
	ligthButton2: BOOL;
	ligthButton3: BOOL;
	
	Lamp1Out: BOOL;
	Lamp2Out: BOOL;
	Lamp3Out: BOOL;
	//some changing temp...
	Temp:OSCAT_BASIC.GEN_SIN;

END_VAR

Lamp1(SwitchIn:= ligthButton1, LampOut=> Lamp1Out);
Lamp2(SwitchIn:= ligthButton2, LampOut=> Lamp2Out);
Lamp3(SwitchIn:= ligthButton3, LampOut=> Lamp3Out);

Temp(
	PT:= T#40S, 
	AM:= 1.0, 
	OS:= 20.0, 
	DL:= 0.0);

Temperature(tempIn:= Temp.Out);
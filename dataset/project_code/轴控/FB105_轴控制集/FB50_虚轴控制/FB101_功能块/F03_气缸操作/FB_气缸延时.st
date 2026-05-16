FUNCTION_BLOCK FB_气缸延时
VAR_INPUT
	Clinyder: BOOL;
	OpenDelayTime: REAL;
	CloseDelayTime: REAL;
	OpenSensor: BOOL;
	CloseSensor: BOOL;
END_VAR
VAR_OUTPUT
	OpenDelay: BOOL;
	CloseDelay: BOOL;
END_VAR
VAR
	TON0: TON;
	TON1: TON;
END_VAR

TON0(IN:= Clinyder , PT:= REAL_TO_TIME(OpenDelayTime*1000), Q=> , ET=> );
TON1(IN:= NOT Clinyder , PT:= REAL_TO_TIME(CloseDelayTime*1000), Q=> , ET=> );

IF TON0.Q THEN
	OpenDelay:=TRUE;
	ELSE
	OpenDelay:=FALSE;	
END_IF

IF TON1.Q THEN
	CloseDelay:=TRUE; 
	ELSE
	CloseDelay:=FALSE;	
END_IF
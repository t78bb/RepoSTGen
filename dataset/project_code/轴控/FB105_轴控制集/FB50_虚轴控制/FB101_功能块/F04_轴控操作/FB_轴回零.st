FUNCTION_BLOCK FB_轴回零
VAR_INPUT
	Excute: BOOL;
	InputSigle: BOOL;
	Emergency: BOOL;
	OffersetDistance: LREAL;
	OffersetVel: LREAL;
	HomeVel: LREAL;
END_VAR

VAR_OUTPUT
	HomeBusy: BOOL;
	HomeDone: BOOL;
	HomeError: BOOL;
END_VAR
VAR
	R_TRIG0: R_TRIG;
	HoneStep: INT;
	MC_MoveRelative0: MC_MoveRelative;
	MC_Stop0: MC_Stop;
	MC_SetPosition0: MC_SetPosition;
	TON0: TON;
	TON1: TON;
	TON2: TON;
END_VAR

VAR_IN_OUT
	AxisName: SM3_BASIC.AXIS_REF_SM3;
END_VAR

MC_MoveRelative0(
	Axis:= AxisName, 
	Execute:= , 
	Distance:= , 
	Velocity:= , 
	Acceleration:= 99999999, 
	Deceleration:= 99999999, 
	Jerk:= , 
	Done=> , 
	Busy=> , 
	CommandAborted=> , 
	Error=> , 
	ErrorID=> );
	
MC_Stop0(
	Axis:= AxisName, 
	Execute:= , 
	Deceleration:= 1000000, 
	Jerk:= , 
	Done=> , 
	Busy=> , 
	Error=> , 
	ErrorID=> );
	
MC_SetPosition0(
	Axis:= AxisName, 
	Execute:= , 
	Position:= 0, 
	Mode:= 0, 
	Done=> , 
	Busy=> , 
	Error=> , 
	ErrorID=> );
	
IF HoneStep<>0 THEN
	HomeBusy:=TRUE;
	ELSE
	HomeBusy:=FALSE;	
END_IF


IF MC_MoveRelative0.Error OR MC_Stop0.Error OR MC_SetPosition0.Error THEN
	HomeError:=TRUE;
	ELSE
	HomeError:=FALSE;	
END_IF

IF Emergency THEN
	HoneStep:=0;
	MC_MoveRelative0.Execute:=FALSE;
	MC_Stop0.Execute:=FALSE;
	MC_SetPosition0.Execute:=FALSE;
	TON0(IN:= FALSE, );
	TON1(IN:= FALSE, );
	TON2(IN:= FALSE, );
	HomeBusy:=FALSE;
	HomeDone:=FALSE;
END_IF

	
R_TRIG0(CLK:= Excute, Q=> );

CASE HoneStep OF
	0:
	IF R_TRIG0.Q THEN
        HomeDone:=FALSE;		
		HoneStep:=1;
	END_IF
	
	1:
	IF NOT InputSigle THEN
		MC_MoveRelative0.Velocity:=HomeVel;
		MC_MoveRelative0.Distance:=-9999999;
		MC_MoveRelative0.Execute:=TRUE;
		HoneStep:=5;
	END_IF
	IF InputSigle THEN
		MC_MoveRelative0.Velocity:=HomeVel;
		MC_MoveRelative0.Distance:=10;		
		MC_MoveRelative0.Execute:=TRUE;
		HoneStep:=10;
	END_IF
	
	5:
	IF MC_MoveRelative0.Execute AND MC_MoveRelative0.Busy AND InputSigle THEN
		MC_MoveRelative0.Execute:=FALSE;
		HoneStep:=15;
	END_IF
	
	10:
	IF MC_MoveRelative0.Execute AND MC_MoveRelative0.Done THEN
		MC_MoveRelative0.Execute:=FALSE;
		HoneStep:=1;
	END_IF
	
	15:
	TON0(IN:= TRUE, PT:= T#0.1S, Q=> , ET=> );
	IF TON0.Q THEN
		MC_Stop0.Execute:=TRUE;
		IF MC_Stop0.Execute AND MC_Stop0.Done THEN
			MC_Stop0.Execute:=FALSE;
			TON0(IN:= FALSE, );
			HoneStep:=20;
		END_IF
	END_IF
	
	20:
	TON2(IN:= TRUE, PT:= T#0.1S, Q=> , ET=> );
	IF TON2.Q THEN
		MC_SetPosition0.Execute:=TRUE;
		IF MC_SetPosition0.Execute AND MC_SetPosition0.Done THEN
			MC_SetPosition0.Execute:=FALSE;
			TON2(IN:= FALSE, );
			HoneStep:=25;
		END_IF
	END_IF	
	
	25:
	TON1(IN:= TRUE, PT:= T#0.1S, Q=> , ET=> );
	IF TON1.Q THEN
		MC_MoveRelative0.Velocity:=OffersetVel;
		MC_MoveRelative0.Distance:=OffersetDistance;		
		MC_MoveRelative0.Execute:=TRUE;
		IF MC_MoveRelative0.Execute AND MC_MoveRelative0.Done THEN
			MC_MoveRelative0.Execute:=FALSE;
			TON1(IN:= FALSE, );
			HoneStep:=30;
		END_IF
	END_IF
	
	30:
	HomeDone:=TRUE;
	HoneStep:=0;
	
	
END_CASE
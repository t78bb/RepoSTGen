PROGRAM Reset
VAR
	fbResetAxisM	:	SM3_Basic.MC_Reset;
	fbResetAxisS	:	SM3_Basic.MC_Reset;
	fbTrigR	:	Standard.R_TRIG;
	bReset	:	BOOL;
END_VAR

fbTrigR(CLK:=IReset);

IF fbTrigR.Q THEN
	bReset:=TRUE;
END_IF

IF bReset THEN
	fbResetAxisM(Axis:=AxisM,Execute:=AxisMSta.bErr);
	fbResetAxisS(Axis:=AxisS,Execute:=AxisSSta.bErr);
	IF (NOT AxisMSta.bErr) AND (NOT AxisSSta.bErr)THEN
		QLedG:=FALSE;
		QLedR:=FALSE;
		QLedY:=TRUE;
		fbResetAxisM(Axis:=AxisM,Execute:=FALSE);
		fbResetAxisS(Axis:=AxisS,Execute:=FALSE);
		bReset:=FALSE;
	END_IF
END_IF
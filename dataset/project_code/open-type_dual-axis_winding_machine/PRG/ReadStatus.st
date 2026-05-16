PROGRAM ReadStatus
VAR
	fbReadStaM	:	SM3_Basic.MC_ReadStatus;
	fbReadStaS	:	SM3_Basic.MC_ReadStatus;
END_VAR

fbReadStaM(Axis:=AxisM,Enable:=TRUE);
fbReadStaS(Axis:=AxisS,Enable:=TRUE);

IF fbReadStaM.Valid THEN
	AxisMSta.bErr := fbReadStaM.Errorstop;
	AxisMSta.bStandStill := fbReadStaM.StandStill;
	AxisMSta.bIsMoving := (NOT fbReadStaM.StandStill) AND (NOT fbReadStaM.Errorstop) AND (fbReadStaM.ConstantVelocity OR fbReadStaM.ContinuousMotion OR fbReadStaM.DiscreteMotion OR fbReadStaM.SynchronizedMotion);
END_IF

IF fbReadStaS.Valid THEN
	AxisSSta.bErr := fbReadStaS.Errorstop;
	AxisSSta.bStandStill := fbReadStaS.StandStill;
	AxisSSta.bIsMoving := (NOT fbReadStaS.StandStill) AND (NOT fbReadStaS.Errorstop) AND (fbReadStaS.ConstantVelocity OR fbReadStaS.ContinuousMotion OR fbReadStaS.DiscreteMotion OR fbReadStaS.SynchronizedMotion);
END_IF

IF IEStop THEN
	MHmiOutMessage := 'Emergency stop';
	QLedG:=FALSE;
	QLedR:=TRUE;
	QLedY:=FALSE;
ELSE
	IF AxisMSta.bErr OR AxisSSta.bErr THEN
		MHmiOutMessage := 'Axis Errors';
		QLedG:=FALSE;
		QLedR:=TRUE;
		QLedY:=FALSE;
	ELSE
		MHmiOutMessage := 'System Normal';
	END_IF
END_IF


MHmiAxisVPos:=DINT_TO_REAL(TRUNC(AxisV.fActPosition * 1000)) / 1000.0;

VAR
	getKinematic : MC_ReadKinTransform;
	screwAxisResult : SM3M.SMC_Frame;
	convertedAxisPos : SM3M.SMC_Vec;
	kinematicResult : SM3M.SMC_Frame;
	cdNotUsed : TRAFO.CONFIGDATA;
END_VAR

convertedAxisPos.a[0] := axisPos.a0 * SM3M.SMC_FACTOR_DEG_TO_RAD;
convertedAxisPos.a[1] := axisPos.a1 * SM3M.SMC_FACTOR_DEG_TO_RAD;
convertedAxisPos.a[2] := axisPos.a2;
convertedAxisPos.n := 3;

SMC_OpenChainKinematics_SolveForward(
	fTCP:= screwAxisResult,
	aS:= m_dynModel.m_aS,
	vJoints:= convertedAxisPos,
	fTCP_init:= ZERO_TCP_FRAME);

getKinematic(
	AxisGroup:= AxisGroup,
	Enable:= TRUE);

IF getKinematic.Valid AND_THEN getKinematic.KinTransform <> 0 THEN
	getKinematic.KinTransform.AxesToCartesian(
		f:= kinematicResult,
		cd:= cdNotUsed,
		a:= axisPos);
	
	IsScrewAxisAndKinematicEqual :=
		ABS(screwAxisResult.vT.dX - kinematicResult.vT.dX) <= epsilon
		AND_THEN ABS(screwAxisResult.vT.dY- kinematicResult.vT.dY) <= epsilon
		AND_THEN ABS(screwAxisResult.vT.dZ - kinematicResult.vT.dZ) <= epsilon;
ELSE
	IsScrewAxisAndKinematicEqual := FALSE;
END_IF
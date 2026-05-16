VAR
	expectedTorque : SM3M.SMC_Vec;
	calculatedTorque : SM3M.SMC_Vec;
	axesState : SM3M.SMC_DynVecState;
	addParams : SMDYN.DynamicsParams;
	i : DINT;
END_VAR
VAR CONSTANT
	EPSILON : LREAL := 1E-10;
END_VAR

m_dynModel.Init();

/// All axes in zero position.
axesState.v.a[0] := 0;
axesState.v.a[1] := 0;
axesState.v.a[2] := 0;
axesState.v.n := axesState.v_s.n := axesState.v_ss.n := 3;

/// Gravitational acceleration in [m/s²]
addParams.g.dZ := 9.81;

/// Expected torque of the revolute axis of arm 1 in [Nm]
expectedTorque.a[0] := 0;
/// Expected torque of the revolute axis of arm 2 in [Nm]
expectedTorque.a[1] := 0;
/// Expected force of the prismatic z-axis in [N]
expectedTorque.a[2] := - m_dynModel.zAxisMass * 9.81;
expectedTorque.n := 3;

m_dynModel.AxesStateToTorque(
	torque:= calculatedTorque,
	axesState:= axesState,
	addParams:= addParams);

CheckStandstillTorque := calculatedTorque.n = expectedTorque.n;
FOR i := 0 TO calculatedTorque.n - 1 DO
	CheckStandstillTorque := CheckStandstillTorque
							 AND_THEN ABS(calculatedTorque.a[i] - expectedTorque.a[i]) <= EPSILON;
END_FOR
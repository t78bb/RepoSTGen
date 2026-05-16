TYPE ST_AxisCtrl :
STRUCT
	bEnable : BOOL ;
	bEnablePostive : BOOL := TRUE;
	bEnableNegtive: BOOL := TRUE;
	rOverride : REAL := 100;
	bStop : BOOL ;
	bHalt  : BOOL ;
	bReset : BOOL ;
	bMoveVelo : BOOL ;
	rVelo : REAL ;
	rPosintonVelo : REAL ;
	bMoveRelative : BOOL ;
	rRelativeDis : REAL ;
	bMoveRelativeDone : BOOL ;
	bMoveAbs : BOOL ;
	rAbsPos  : REAL ;
	bMoveAbsDone : BOOL ;
	bMoveModulo :BOOL ;
	rModuloPos : REAL ;
	bMoveModuloDone: BOOL ;
	bHomeExe : BOOL;
	rHomePos : REAL ;
	bCalibrationCam: BOOL ; 
	bJogFwd : BOOL ;
	bJogBwd : BOOL;
	rJogVelo : REAL  ;
	bSetPos : BOOL ;
	bSetPosDone: BOOL ;
	rSetPos : REAL ;
	Direction : MC_Direction;
	Acceleration: REAL ;
	Deceleration:REAL ;
	Jerk:REAL;
	bPosLimit : BOOL ; 
	bNegLimit : BOOL ; 
	bError:BOOL;
	bErrorStop:BOOL;
	bStandstill:BOOL;
	bAccing:BOOL;
	bDecing:BOOL;
	bSynchronized:BOOL;
	rActVel: REAL;
	rActPos: REAL;
END_STRUCT
END_TYPE

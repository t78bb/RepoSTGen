{attribute 'qualified_only'}
VAR_GLOBAL
	// inputs
	FIO_iMovingX: BOOL;
	FIO_iMovingZ: BOOL;
	FIO_iItemDetected: BOOL;
	FIO_iLidAtPlace: BOOL;
	FIO_iBaseAtPlace: BOOL;
	FIO_iPartLeaving: BOOL;
	FIO_iLidClamped: BOOL;
	FIO_iLidPosAtLimit: BOOL;
	FIO_iBaseClamped: BOOL;
	FIO_iBasePosAtLimit: BOOL;
	FIO_iReset: BOOL;
	
	//outputs
	FIO_oLidsConveyor: BOOL;
	FIO_oBasesConveyor: BOOL;
	FIO_oMoveX: BOOL;
	FIO_oMoveZ: BOOL;
	FIO_oGrab: BOOL;
	FIO_oClampLid: BOOL;
	FIO_oLidPosRaise: BOOL;
	FIO_oClampBase: BOOL;
	FIO_oBasePosRaise: BOOL;
	FIO_oCounter: WORD;
END_VAR
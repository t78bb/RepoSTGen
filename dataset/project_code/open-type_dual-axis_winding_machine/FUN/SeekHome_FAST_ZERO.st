METHOD FAST_ZERO
VAR_IN_OUT 
	_Axis	:	AXIS_REF_SM3;
END_VAR
VAR_INPUT
	_xHome	:	BOOL;
	_xAbort	:	BOOL;
	_nHomeMode	:	HomeMode;
	_fFastHomeVel	:	LREAL;
	_fSlowHomeVel	:	LREAL;
	_fHomeAcc		:	LREAL;
	_fHomeDec		:	LREAL;
	_fHomePos		:	LREAL;
	_xReferenceSwitch	:	BOOL;//typically is true
	_nDirection	:	MC_DIRECTION;
	_xIndexPulse	:	BOOL;
END_VAR
VAR_OUTPUT
	_xBusy	:	BOOL;
	_xDone	:	BOOL;
	_xErr	:	BOOL;
	_iErrId	:	DINT;
END_VAR
VAR
	_fbMoveVel	:	MC_MoveVelocity;
	_fbMoveAbs	:	MC_MoveAbsolute;
	_fbHalt		:	MC_Halt;
	_fbSetPos	:	MC_SetPosition;
	_fbRtrig		:	R_TRIG;
	_fbFtrig		:	F_TRIG;
	_nBDirection	:	MC_DIRECTION;
	_fTempPos		:	LREAL;
	_nState		:	USINT;
	fbRtrig	:	R_TRIG;
END_VAR


CASE _nState OF
	21:
		_fbMoveAbs(Execute := TRUE,Axis := _Axis,Position := _fTempPos,Velocity := _fFastHomeVel,Acceleration := _fHomeAcc,Deceleration := _fHomeDec);
		IF _fbMoveAbs.Done THEN
			_fbMoveAbs(Execute := FALSE,Axis := _Axis);
			_nState := 100;
		END_IF
		IF _fbMoveAbs.Error THEN//meet error
			_nState := 200;
			_iErrId := _fbMoveAbs.ErrorID;
		END_IF
END_CASE

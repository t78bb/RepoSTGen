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

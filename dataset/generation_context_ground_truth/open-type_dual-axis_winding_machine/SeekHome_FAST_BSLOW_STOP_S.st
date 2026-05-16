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
	1:
		IF _xReferenceSwitch THEN
			_nState := 2;//out of ReferenceSwitch
		ELSE
			_nState :=3;//in the ReferenceSwitch
		END_IF
		
		_fbMoveAbs(Execute := FALSE,Axis := _Axis);
		_fbSetPos(Execute := FALSE,Axis := _Axis);
		_fbMoveVel(Execute := FALSE,Axis := _Axis);
	2://move out of the ReferenceSwitch
		_fbMoveVel(Execute := TRUE,Axis := _Axis,Velocity := _fSlowHomeVel,Acceleration := _fHomeAcc,Deceleration := _fHomeDec,Direction := _nBDirection);
		IF _fbFtrig.Q THEN//left the ReferenceSwitch
			_fTempPos := _Axis.fActPosition;//save the position
			_fbMoveVel(Execute := FALSE,Axis := _Axis);
			_nState := 50;
		END_IF
		IF _fbMoveVel.Error THEN//meet error
			_iErrId := _fbMoveVel.ErrorID;
			_fbMoveVel(Execute := FALSE,Axis := _Axis);
			_nState := 200;
		END_IF

	3://move to ReferenceSwitch
		_fbMoveVel(Execute := TRUE,Axis := _Axis,Velocity := _fFastHomeVel,Acceleration := _fHomeAcc,Deceleration := _fHomeDec,Direction := _nDirection);
		IF _fbRtrig.Q THEN//arrive the ReferenceSwitch
			_fbMoveVel(Execute := FALSE,Axis := _Axis);
			_nState := 2;
		END_IF
		IF _fbMoveVel.Error THEN//meet error
			_iErrId := _fbMoveVel.ErrorID;
			_fbMoveVel(Execute := FALSE,Axis := _Axis);
			_nState := 200;
		END_IF
END_CASE

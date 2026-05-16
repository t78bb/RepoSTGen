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
	11:
		IF _xReferenceSwitch THEN
			_nState := 13;//out of ReferenceSwitch
		ELSE
			_nState :=12;//in the ReferenceSwitch
		END_IF
		
		_fbMoveAbs(Execute := FALSE,Axis := _Axis);
		_fbSetPos(Execute := FALSE,Axis := _Axis);
		_fbMoveVel(Execute := FALSE,Axis := _Axis);
	12://move out of the ReferenceSwitch
		_fbMoveVel(Execute := TRUE,Axis := _Axis,Velocity := _fSlowHomeVel,Acceleration := _fHomeAcc,Deceleration := _fHomeDec,Direction := _nDirection);
		IF _fbRtrig.Q THEN//left the ReferenceSwitch
			_fTempPos := _Axis.fActPosition;//save the position
			_fbMoveVel(Execute := FALSE,Axis := _Axis);
			_nState := 50;
		END_IF
		IF _fbMoveVel.Error THEN//meet error
			_iErrId := _fbMoveVel.ErrorID;
			_fbMoveVel(Execute := FALSE,Axis := _Axis);
			_nState := 200;
		END_IF
	13://move to ReferenceSwitch
		_fbMoveVel(Execute := TRUE,Axis := _Axis,Velocity := _fFastHomeVel,Acceleration := _fHomeAcc,Deceleration := _fHomeDec,Direction := _nDirection);
		IF _fbFtrig.Q THEN//arrive the ReferenceSwitch
			_fbMoveVel(Execute := FALSE,Axis := _Axis);
			_nState := 12;
		END_IF
		IF _fbMoveVel.Error THEN//meet error
			_iErrId := _fbMoveVel.ErrorID;
			_fbMoveVel(Execute := FALSE,Axis := _Axis);
			_nState := 200;
		END_IF
	50:
		_fbMoveAbs(Execute := TRUE,Axis := _Axis,Position := _fTempPos,Velocity := _fSlowHomeVel,Acceleration := _fHomeAcc,Deceleration := _fHomeDec);
		IF _fbMoveAbs.Done THEN
			_fbMoveAbs(Execute := FALSE,Axis := _Axis);
			_nState := 100;
		END_IF
		IF _fbMoveAbs.Error THEN//meet error
			_nState := 200;
			_iErrId := _fbMoveAbs.ErrorID;
		END_IF
	100:
		_fbSetPos(Execute := TRUE,Axis := _Axis,Position := _fHomePos,Mode := FALSE);//set absolute position
		IF _fbSetPos.Done THEN
			_fbSetPos(Execute := FALSE,Axis := _Axis);
			_xDone := TRUE;
			_xBusy := FALSE;
			_nState := 0;
		END_IF
		IF _fbSetPos.Error THEN//meet error
			_iErrId := _fbSetPos.ErrorID;
			_nState := 200;
		END_IF
	200:
		_xErr := TRUE;
		_xBusy := FALSE;
		_nState := 0;
END_CASE

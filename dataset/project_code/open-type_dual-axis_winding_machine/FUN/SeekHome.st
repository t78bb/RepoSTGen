FUNCTION_BLOCK SeekHome
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

//check left / arrive the ReferenceSwitch
_fbRtrig(CLK := _xReferenceSwitch);
_fbFtrig(CLK := _xReferenceSwitch);
fbRtrig(CLK := _xHome);

IF NOT _xHome THEN
	_fbMoveVel(Axis := _Axis,Execute := FALSE);
	_fbMoveAbs(Axis := _Axis,Execute := FALSE);
	_fbHalt(Axis := _Axis,Execute := FALSE);
	_fbSetPos(Axis := _Axis,Execute := FALSE);
	_xDone := FALSE;
	_xErr := FALSE;
END_IF

CASE _nState OF
	0:
		IF fbRtrig.Q THEN
			_xBusy := TRUE;
			_xDone := FALSE;
			_xErr := FALSE;
			_iErrId := 0;
		
			CASE _nDirection OF //cal which is the invert direction
				MC_DIRECTION.positive:
					_nBDirection := MC_DIRECTION.negative;
				MC_DIRECTION.negative:
					_nBDirection := MC_DIRECTION.positive;
				ELSE
					_xErr := TRUE;
			END_CASE
			
			CASE _nHomeMode OF
				HomeMode.FAST_ZERO:
					_fTempPos := 0;
					_nState := 21;
				HomeMode.FAST_BSLOW_STOP_S:
					_nState := 1;
				HomeMode.FAST_SLOW_STOP_S:
					_nState := 11;
				HomeMode.FAST_BSLOW_I_STOP_S:
					_nState := 31;
				HomeMode.FAST_SLOW_I_STOP_S:
					_nState := 41;
			END_CASE
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

FAST_ZERO();
FAST_BSLOW_STOP_S();
FAST_SLOW_STOP_S();
FAST_BSLOW_I_STOP_S();
FAST_SLOW_I_STOP_S();
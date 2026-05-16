FUNCTION_BLOCK StarWork
VAR_IN_OUT 
	_AxisW	:	AXIS_REF_SM3;
	_AxisU	:	AXIS_REF_SM3;
	_AxisV	:	AXIS_REF_SM3;
END_VAR
VAR_INPUT
	_bStart	:	BOOL;
	_bStop	:	BOOL;
	_bCheckR	:	BOOL;
	_bFFlag		:	BOOL;
	_lD		:	LREAL;
	_lTk	:	LREAL;
	_lVel	:	LREAL;
	_nDirection	:	MC_DIRECTION;
END_VAR
VAR_OUTPUT
	_xDone	:	BOOL;
	_xErr	:	BOOL;
	_iErrId	:	DINT;
END_VAR
VAR
	_fbAxisWMoveRel	:	SM3_Basic.MC_MoveRelative;
	_fbAxisUMoveRel	:	SM3_Basic.MC_MoveRelative;
	_fbAxisWMoveVelocity: SM3_Basic.MC_MoveVelocity;
	_fbAxisUMoveVelocity: SM3_Basic.MC_MoveVelocity;
	_fbAxisWFollowVelocity:SM3_Basic.SMC_FollowVelocity;
	_fbAxisUFollowVelocity:SM3_Basic.SMC_FollowVelocity;
	_fbHaltAxisW		:	MC_Halt;
	_fbHaltAxisU		:	MC_Halt;
	_fbStartRtrig	:	R_TRIG;
	_fbStopRtrig		:	R_TRIG;
	_fbCheckRtrig		:	R_TRIG;
	_AxisPID:Util.PID_FIXCYCLE;
	
	AxisWVel:LREAL;
	AxisUVel:LREAL;
	AxisWOldPoint,AxisWNewPoint:LREAL;
	AxisUOldPoint,AxisUNewPoint:LREAL;
	AxisVOldPoint,AxisVNewPoint:LREAL;

	_iStatus :	INT;
	Hold,Hnew:LREAL;
	Lold,Lnew:LREAL;
	Wr,Ur:LREAL;//半径
	PIDOut: REAL;
END_VAR

CASE _iStatus OF
	3:
		_fbAxisWMoveVelocity(Axis:=_AxisW,Execute:=TRUE,Velocity:=20,Acceleration:=3600,Deceleration:=3600,Direction:=-1);
		IF _AxisV.fActPosition>=211 THEN
			_fbAxisWMoveVelocity(Axis:=_AxisW,Execute:=FALSE);
			_fbHaltAxisW(Axis:=_AxisW,Execute:=FALSE,Deceleration:=3600);
			_iStatus:=4;
		END_IF
	4:
		_fbHaltAxisW(Axis:=_AxisW,Deceleration:=3600,Execute:=TRUE);
		IF _fbHaltAxisW.Done THEN
			_iStatus:=5;
		END_IF
		
	5://半径测量初始化
	Hold:=_AxisV.fActPosition;
	_fbCheckRtrig(CLK:=_bCheckR);
	IF _fbCheckRtrig.Q THEN
		_fbAxisWMoveRel(Axis:=_AxisW,Execute:=FALSE);
		_fbAxisUMoveRel(Axis:=_AxisU,Execute:=FALSE);
		_iStatus:=6;
	END_IF
		6:
		Hold:=_AxisV.fActPosition;
		_iStatus:=7;
	7:
		_fbAxisUMoveRel(Axis:=_AxisU,Execute:=TRUE,Distance:=360,Velocity:=10,Deceleration:=3600,Acceleration:=3600);
		IF _fbAxisUMoveRel.Done THEN
			Hnew:=_AxisV.fActPosition;
			_fbAxisUMoveRel(Axis:=_AxisU,Execute:=FALSE);
			_iStatus:=8;
		END_IF
	8:
		Ur:=ABS(SQRT(EXPT(_lD,2)+EXPT(Hnew+31,2))-SQRT(EXPT(_lD,2)+EXPT(Hold+31,2)))/SMC_PI+_lTk;
		Hold:=_AxisV.fActPosition;
		_iStatus:=9;

	9://半径测量
		_fbAxisWMoveRel(Axis:=_AxisW,Execute:=TRUE,Distance:=-360,Velocity:=10,Acceleration:=3600,Deceleration:=3600);
		IF _fbAxisWMoveRel.Done THEN
			Hnew:=_AxisV.fActPosition;
			_fbAxisWMoveRel(Axis:=_AxisW,Execute:=FALSE);
			_iStatus:=10;
		END_IF
	10:
		Wr:=ABS(SQRT(EXPT(_lD,2)+EXPT(Hnew+31,2))-SQRT(EXPT(_lD,2)+EXPT(Hold+31,2)))/SMC_PI+_lTk;
		   _iStatus:=11;
	11:
		AxisWVel:=_lVel;
		AxisUVel:=-1*AxisWVel*Wr/Ur;
		AxisWOldPoint:=_AxisW.fActPosition;
		AxisUOldPoint:=_AxisU.fActPosition;
		AxisVOldPoint:=_AxisV.fActPosition;
		_iStatus:=12;

	
	12:
		IF AxisWOldPoint>_AxisW.fActPosition THEN
			AxisWVel:=AxisWVel+AxisWVel*_lTk/(Wr-_lTk);
		END_IF
		IF AxisUOldPoint>_AxisU.fActPosition THEN
			AxisUVel:=AxisUVel-AxisUVel*_lTk/(Ur+_lTk);
		END_IF
		_fbAxisWFollowVelocity(Axis:=_AxisW,bExecute:=TRUE,fSetVelocity:=AxisWVel);
		_fbAxisUFollowVelocity(Axis:=_AxisU,bExecute:=TRUE,fSetVelocity:=AxisUVel);
		_AxisPID(ACTUAL:=AxisV.fActPosition,SET_POINT:=AxisVOldPoint,KP:=0.05,TN:=5,TV:=0,CYCLE:=0.004,Y=>PIDOut);
		AxisUVel:=AxisUVel-PIDOut;
		AxisWOldPoint:=_AxisW.fActPosition;
		AxisUOldPoint:=_AxisU.fActPosition;
END_CASE
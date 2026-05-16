PROGRAM PLC_PRG
VAR
	fbSeekHome	:	SeekHome;
	fbPowerAxisM	:	SM3_Basic.MC_Power;
	fbPowerAxisS	:	SM3_Basic.MC_Power;
	fbAxisMMoveRel	:	SM3_Basic.MC_MoveRelative;
	fbAxisSMoveRel	:	SM3_Basic.MC_MoveRelative;
	fbSetPosAxisV	:	SM3_Basic.MC_SetPosition;
	fbAxisMMoveVelocity: SM3_Basic.MC_MoveVelocity;
	fbAxisSMoveVelocity: SM3_Basic.MC_MoveVelocity;
	fbAxisMFollowVelocity:SM3_Basic.SMC_FollowVelocity;
	fbAxisSFollowVelocity:SM3_Basic.SMC_FollowVelocity;
	AxisMVel:LREAL;
	AxisSVel:LREAL;
	AxisMOldPoint,AxisMNewPoint:LREAL;
	AxisSOldPoint,AxisSNewPoint:LREAL;
	AxisVOldPoint,AxisVNewPoint:LREAL;
	fbHaltAxisM		:	MC_Halt;
	fbHaltAxisS		:	MC_Halt;
	fbStartRtrig	:	R_TRIG;
	fbStopRtrig		:	R_TRIG;
	fbLIORtrig		:	F_TRIG;
	fbRIORtrig		:	F_TRIG;
	fbChaneModeFtrig:	Standard.F_TRIG;
	fbDisplay	:	StaDisplay;
	fbCheckF	:	CheckF;
	bPowerOn	:	BOOL;
	bOKPowerOn	:	BOOL;
	bGoHome	:	BOOL;
	bGoHomeDone	:	BOOL;
	bModeChang	:	BOOL;
	iStatus :	INT;
	bErr	:	BOOL;
	Hold,Hnew:LREAL;
	Lold,Lnew:LREAL;
	D:LREAL:=122.5;
	Mr,Sr:LREAL;//半径
	Tk:LREAL:=0.6;//厚度
	AxisPID1,AxisPID2:Util.PID_FIXCYCLE;
	PIDOut: REAL;
END_VAR

fbPowerAxisM(Axis:=AxisM,Enable:=TRUE,bRegulatorOn:=bPowerOn,bDriveStart:=bPowerOn);
fbPowerAxisS(Axis:=AxisS,Enable:=TRUE,bRegulatorOn:=bPowerOn,bDriveStart:=bPowerOn);
bOKPowerOn:=fbPowerAxisM.Status AND fbPowerAxisS.Status;

fbStopRtrig(CLK := IStop);
IF fbStopRtrig.Q OR IEStop OR AxisMSta.bErr OR AxisSSta.bErr THEN//判断是否按下停止按钮
	fbHaltAxisM(Axis:=AxisM,Execute:=FALSE);
	fbHaltAxisS(Axis:=AxisS,Execute:=FALSE);
	iStatus := 100;
END_IF

IF bOKPowerOn THEN
	IF MHmiModeChange THEN //自动
		QLedG:=TRUE;
		QLedR:=FALSE;
		QLedY:=FALSE;
		CASE iStatus OF
		0://回零初始化
			IF bGoHome THEN
				iStatus:=1;
				bGoHome:=FALSE;
				fbSetPosAxisV(Axis:=AxisV,Execute:=FALSE,Position:=61);
				fbSeekHome(_xHome := FALSE,_xAbort := FALSE,_nHomeMode := 1,_fFastHomeVel := MHmiInHomeVel,_fSlowHomeVel := 5,_fHomeAcc := 3600,
					   _fHomeDec := 3600,_fHomePos := 0,_xReferenceSwitch :=IOri,_Axis := AxisM,_nDirection := MC_DIRECTION.positive);
			END_IF
		1://回零
			fbSeekHome(_xHome := TRUE,_xReferenceSwitch := IOri,_Axis := AxisM);
			IF fbSeekHome._xDone THEN
				fbSetPosAxisV(Axis:=AxisV,Execute:=TRUE,Position:=61);
				IF fbSetPosAxisV.Done THEN
					bGoHomeDone:=TRUE;
					iStatus := 111;
				END_IF
			END_IF
			bErr:=bErr OR fbSeekHome._xErr OR fbSetPosAxisV.Error;
			IF bErr THEN
				fbSeekHome(_xHome := FALSE,_xAbort:=TRUE,_Axis := AxisM);
				iStatus := 100;	
			END_IF
		111://开始执行
			fbStartRtrig(CLK:=IRun);
			IF fbStartRtrig.Q THEN
				iStatus:=2;
			END_IF
		2://向60度位置运动
			fbAxisMMoveVelocity(Axis:=AxisM,Execute:=FALSE);
			IF AxisV.fActPosition>211 THEN
				iStatus:=221;
			ELSE
				iStatus:=222;
			END_IF
		221:
			fbAxisMMoveVelocity(Axis:=AxisM,Execute:=TRUE,Velocity:=25,Acceleration:=3600,Deceleration:=3600,Direction:=1);
			IF AxisV.fActPosition<=211 THEN
				fbAxisMMoveVelocity(Axis:=AxisM,Execute:=FALSE);
				fbHaltAxisM(Axis:=AxisM,Execute:=FALSE,Deceleration:=3600);
				iStatus:=3;
			END_IF
		222:
			fbAxisMMoveVelocity(Axis:=AxisM,Execute:=TRUE,Velocity:=25,Acceleration:=3600,Deceleration:=3600,Direction:=-1);
			IF AxisV.fActPosition>=211 THEN
				fbAxisMMoveVelocity(Axis:=AxisM,Execute:=FALSE);
				fbHaltAxisM(Axis:=AxisM,Execute:=FALSE,Deceleration:=3600);
				iStatus:=3;
			END_IF
		3://到达60度位置后停止
			fbHaltAxisM(Axis:=AxisM,Deceleration:=3600,Execute:=TRUE);
			IF fbHaltAxisM.Done THEN
				iStatus:=4;
			END_IF
		4://半径测量初始化
			Hold:=AxisV.fActPosition;
			fbAxisMMoveRel(Axis:=AxisM,Execute:=FALSE);
			fbAxisSMoveRel(Axis:=AxisS,Execute:=FALSE);
			iStatus:=5;
		5://半径测量
			Hold:=AxisV.fActPosition;
			iStatus:=6;
		6:
			fbAxisSMoveRel(Axis:=AxisS,Execute:=TRUE,Distance:=360,Velocity:=25,Deceleration:=3600,Acceleration:=3600);
			IF fbAxisSMoveRel.Done THEN
				Hnew:=AxisV.fActPosition;
				fbAxisSMoveRel(Axis:=AxisS,Execute:=FALSE);
				iStatus:=7;
			END_IF
		7:
			// 使用F_CalculateRadius函数计算从轴半径
			Sr := F_CalculateRadius(lD:=D, lHold:=Hold, lHnew:=Hnew, lTk:=Tk, lOffset:=31);
			Hold:=AxisV.fActPosition;
			iStatus:=8;
		8:
			fbAxisMMoveRel(Axis:=AxisM,Execute:=TRUE,Distance:=-360,Velocity:=25,Acceleration:=3600,Deceleration:=3600);
			IF fbAxisMMoveRel.Done THEN
				Hnew:=AxisV.fActPosition;
				fbAxisMMoveRel(Axis:=AxisM,Execute:=FALSE);
				iStatus:=9;
			END_IF
		9:
			// 使用F_CalculateRadius函数计算主轴半径
			Mr := F_CalculateRadius(lD:=D, lHold:=Hold, lHnew:=Hnew, lTk:=Tk, lOffset:=31);
			iStatus:=10;
		10://初始速度
			AxisMVel:=MHmiInVel;
			AxisSVel:=-1*AxisMVel*Mr/Sr;
			AxisMOldPoint:=AxisM.fActPosition;
			AxisSOldPoint:=AxisS.fActPosition;
			AxisVOldPoint:=AxisV.fActPosition;
			AxisPID1(RESET:=TRUE);
			iStatus:=11;		
		11://同步控制
			// 使用F_CompensateVelocity函数进行速度补偿
			AxisMVel := F_CompensateVelocity(lCurrentVel:=AxisMVel, lOldPos:=AxisMOldPoint, lNewPos:=AxisM.fActPosition, lRadius:=Mr, lTk:=Tk, bUnwinding:=TRUE);
			AxisSVel := F_CompensateVelocity(lCurrentVel:=AxisSVel, lOldPos:=AxisSOldPoint, lNewPos:=AxisS.fActPosition, lRadius:=Sr, lTk:=Tk, bUnwinding:=FALSE);
			
			fbAxisMFollowVelocity(Axis:=AxisM,bExecute:=TRUE,fSetVelocity:=AxisMVel);
			fbAxisSFollowVelocity(Axis:=AxisS,bExecute:=TRUE,fSetVelocity:=AxisSVel);
			AxisPID1(ACTUAL:=AxisV.fActPosition,SET_POINT:=AxisVOldPoint,KP:=0.1,RESET:=FALSE,TN:=3,TV:=0,CYCLE:=0.004,Y=>PIDOut);
		//	AxisMVel:=AxisMVel+PIDOut;
			AxisSVel:=AxisSVel-PIDOut;
			AxisMOldPoint:=AxisM.fActPosition;
			AxisSOldPoint:=AxisS.fActPosition;
			fbLIORtrig(CLK:=LFlage);
			IF fbLIORtrig.Q THEN
				fbAxisMFollowVelocity(Axis:=AxisM,bExecute:=FALSE);
				fbAxisSFollowVelocity(Axis:=AxisS,bExecute:=FALSE);
				fbHaltAxisM(Axis:=AxisM,Execute:=FALSE);
				fbHaltAxisS(Axis:=AxisS,Execute:=FALSE);
				iStatus:=12;
			END_IF
			fbCheckF(lM:=MHmiInG,lL:=122.5,lH:=AxisV.fActPosition,lF=>MHmiOutF);
		12://右限位
			fbHaltAxisM(Axis:=AxisM,Execute:=TRUE,Deceleration:=36000);
			fbHaltAxisS(Axis:=AxisS,Execute:=TRUE,Deceleration:=36000);
			IF fbHaltAxisM.Done AND fbHaltAxisS.Done THEN
				iStatus:=13;
			END_IF
		13://开始反向卷绕
			fbAxisSMoveVelocity(Axis:=AxisS,Execute:=FALSE);
			IF AxisV.fActPosition>211 THEN
				iStatus:=14;
			ELSE
				iStatus:=15;
			END_IF
		14:
			fbAxisSMoveVelocity(Axis:=AxisS,Execute:=TRUE,Velocity:=25,Acceleration:=3600,Deceleration:=3600,Direction:=1);
			IF AxisV.fActPosition<=211 THEN
				fbAxisSMoveVelocity(Axis:=AxisS,Execute:=FALSE);
				fbHaltAxisS(Axis:=AxisS,Execute:=FALSE,Deceleration:=3600);
				iStatus:=16;
			END_IF
		15:
			fbAxisSMoveVelocity(Axis:=AxisS,Execute:=TRUE,Velocity:=25,Acceleration:=3600,Deceleration:=3600,Direction:=-1);
			IF AxisV.fActPosition>=211 THEN
				fbAxisSMoveVelocity(Axis:=AxisS,Execute:=FALSE);
				fbHaltAxisS(Axis:=AxisS,Execute:=FALSE,Deceleration:=3600);
				iStatus:=16;
			END_IF
		16:
			fbHaltAxisS(Axis:=AxisS,Deceleration:=3600,Execute:=TRUE);
			IF fbHaltAxisS.Done THEN
				fbHaltAxisS(Axis:=AxisS,Execute:=FALSE,Deceleration:=3600);
				iStatus:=17;
			END_IF
		17:
			Hold:=AxisV.fActPosition;
			fbAxisMMoveRel(Axis:=AxisM,Execute:=FALSE);
			fbAxisSMoveRel(Axis:=AxisS,Execute:=FALSE);
			iStatus:=18;
		18:
			fbAxisMMoveRel(Axis:=AxisM,Execute:=TRUE,Distance:=360,Velocity:=25,Deceleration:=3600,Acceleration:=3600);
			IF fbAxisMMoveRel.Done THEN
				Hnew:=AxisV.fActPosition;
				fbAxisMMoveRel(Axis:=AxisS,Execute:=FALSE);
				iStatus:=19;
			END_IF
		19:
			// 使用F_CalculateRadius函数计算主轴半径
			Mr := F_CalculateRadius(lD:=D, lHold:=Hold, lHnew:=Hnew, lTk:=Tk, lOffset:=31);
			Hold:=AxisV.fActPosition;
			iStatus:=20;
		20:
			fbAxisSMoveRel(Axis:=AxisS,Execute:=TRUE,Distance:=-360,Velocity:=25,Acceleration:=3600,Deceleration:=3600);
			IF fbAxisSMoveRel.Done THEN
				Hnew:=AxisV.fActPosition;
				fbAxisSMoveRel(Axis:=AxisS,Execute:=FALSE);
				iStatus:=21;
			END_IF
		21:
			// 使用F_CalculateRadius函数计算从轴半径
			Sr := F_CalculateRadius(lD:=D, lHold:=Hold, lHnew:=Hnew, lTk:=Tk, lOffset:=31);
			iStatus:=22;
		22:
			AxisSVel:=MHmiInVel;
			AxisMVel:=-1*AxisSVel*Sr/Mr;
			AxisMOldPoint:=AxisM.fActPosition;
			AxisSOldPoint:=AxisS.fActPosition;
			AxisVOldPoint:=AxisV.fActPosition;
			AxisPID2(RESET:=TRUE);
			iStatus:=23;
		23:
			// 使用F_CompensateVelocity函数进行速度补偿（反向）
			AxisSVel := F_CompensateVelocity(lCurrentVel:=AxisSVel, lOldPos:=AxisSOldPoint, lNewPos:=AxisS.fActPosition, lRadius:=Sr, lTk:=Tk, bUnwinding:=TRUE);
			AxisMVel := F_CompensateVelocity(lCurrentVel:=AxisMVel, lOldPos:=AxisMOldPoint, lNewPos:=AxisM.fActPosition, lRadius:=Mr, lTk:=Tk, bUnwinding:=FALSE);
			
			fbAxisMFollowVelocity(Axis:=AxisM,bExecute:=TRUE,fSetVelocity:=AxisMVel);
			fbAxisSFollowVelocity(Axis:=AxisS,bExecute:=TRUE,fSetVelocity:=AxisSVel);
			AxisPID2(ACTUAL:=AxisV.fActPosition,SET_POINT:=AxisVOldPoint,KP:=0.1,TN:=3,TV:=0,RESET:=FALSE,CYCLE:=0.004,Y=>PIDOut);
			//AxisSVel:=AxisSVel+PIDOut;
			AxisMVel:=AxisMVel-PIDOut;
			AxisMOldPoint:=AxisM.fActPosition;
			AxisSOldPoint:=AxisS.fActPosition;
			fbRIORtrig(CLK:=RFlage);
			IF fbRIORtrig.Q THEN
				fbAxisMFollowVelocity(Axis:=AxisM,bExecute:=FALSE);
				fbAxisSFollowVelocity(Axis:=AxisS,bExecute:=FALSE);
				fbHaltAxisM(Axis:=AxisM,Execute:=FALSE);
				fbHaltAxisS(Axis:=AxisS,Execute:=FALSE);
				iStatus:=24;
			END_IF
			fbCheckF(lM:=MHmiInG,lL:=122.5,lH:=AxisV.fActPosition,lF=>MHmiOutF);
		24:
			fbHaltAxisM(Axis:=AxisM,Execute:=TRUE,Deceleration:=36000);
			fbHaltAxisS(Axis:=AxisS,Execute:=TRUE,Deceleration:=36000);
			IF fbHaltAxisM.Done AND fbHaltAxisS.Done THEN
				fbAxisMMoveRel(Axis:=AxisM,Execute:=FALSE);
				fbAxisSMoveRel(Axis:=AxisS,Execute:=FALSE);
				iStatus:=2;
			END_IF
		100://错误处理
			fbHaltAxisM(Axis:=AxisM,Execute:=TRUE,Deceleration:=36000);
			fbHaltAxisS(Axis:=AxisS,Execute:=TRUE,Deceleration:=36000);
			IF fbHaltAxisS.Done THEN
				fbHaltAxisM(Axis:=AxisM,Execute:=FALSE);
				fbHaltAxisS(Axis:=AxisS,Execute:=FALSE);
				bGoHomeDone:=FALSE;
				iStatus:=0;
			END_IF
		END_CASE
	ELSE //手动
		QLedG:=FALSE;
		QLedR:=FALSE;
		QLedY:=TRUE;
		JOG();
	END_IF
END_IF

IF MHmiModeChange THEN
	MHmiOutModeNo:=1;
ELSE
	MHmiOutModeNo:=0;
END_IF

fbChaneModeFtrig(CLK:=MHmiModeChange);
IF fbChaneModeFtrig.Q THEN
	bModeChang:=TRUE;
END_IF

IF bModeChang THEN
	fbHaltAxisM(Axis:=AxisM,Execute:=TRUE,Deceleration:=36000);
	fbHaltAxisS(Axis:=AxisS,Execute:=TRUE,Deceleration:=36000);
	IF fbHaltAxisS.Done THEN
		fbHaltAxisM(Axis:=AxisM,Execute:=FALSE);
		fbHaltAxisS(Axis:=AxisS,Execute:=FALSE);
		bModeChang:=FALSE;
		bGoHomeDone:=FALSE;
		iStatus:=0;
	END_IF
END_IF

ReadStatus();
Reset();
fbDisplay(iStatus:=iStatus,Y1=>MHmiLed1,Y2=>MHmiLed2,Y3=>MHmiLed3,Y4=>MHmiLed4,Y5=>MHmiRGo,Y6=>MHmiLGo);
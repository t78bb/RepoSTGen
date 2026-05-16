PROGRAM PLC_PRG
VAR
	(* 使用重构后的功能块 *)
	fbDualAxisPower			:	FB_DualAxisPower;			// 双轴电源管理
	fbDualAxisEmergencyStop	:	FB_DualAxisEmergencyStop;	// 双轴紧急停止
	
	fbSeekHome				:	SeekHome;					// 回零功能块
	fbSetPosAxisV			:	SM3_Basic.MC_SetPosition;	// 轴V位置设置
	fbStopRtrig				:	R_TRIG;						// 停止上升沿检测
	
	bPowerOn				:	BOOL;						// 电源使能
	bOKPowerOn				:	BOOL;						// 电源就绪
	bStart					:	BOOL;						// 启动信号
	bStop					:	BOOL;						// 停止信号
	bGoHome					:	BOOL;						// 回零信号
	bGoHomeDone				:	BOOL;						// 回零完成
	bCheckR					:	BOOL;						// 检查半径
	iStatus					:	INT;						// 状态机
	bErr					:	BOOL;						// 错误标志
	
	D						:	LREAL := 122.5;				// 轴间距
	Tk						:	LREAL := 0.6;				// 材料厚度
	
END_VAR

// 使用FB_DualAxisPower进行双轴电源管理
fbDualAxisPower(
	AxisM := AxisM,
	AxisS := AxisS,
	bPowerOn := bPowerOn
);
bOKPowerOn := fbDualAxisPower.bReady;

// 停止按钮检测
fbStopRtrig(CLK := bStop);
IF fbStopRtrig.Q THEN // 判断是否按下停止按钮
	iStatus := 100; // 跳转到紧急停止状态
END_IF

IF bOKPowerOn THEN
	CASE iStatus OF
	0:
	1:
	//回零初始化
	IF bGoHome THEN
		iStatus:=2;
		bGoHome:=FALSE;
		fbSetPosAxisV(Axis:=AxisV,Execute:=FALSE,Position:=61);
		fbSeekHome(_xHome := FALSE,_xAbort := FALSE,_nHomeMode := 1,_fFastHomeVel := MHmiInHomeVel,_fSlowHomeVel := 5,_fHomeAcc := 3600,
			       _fHomeDec := 3600,_fHomePos := 0,_xReferenceSwitch := IOri,_Axis := AxisM,_nDirection := MC_DIRECTION.negative);
	END_IF
	2://回零
	fbSeekHome(_xHome := TRUE,_xReferenceSwitch := IOri,_Axis := AxisM);
	IF fbSeekHome._xDone THEN
		fbSetPosAxisV(Axis:=AxisV,Execute:=TRUE,Position:=54);
		IF fbSetPosAxisV.Done THEN
			bGoHomeDone:=TRUE;
			iStatus := 3;
		END_IF
	END_IF
	bErr:=bErr OR fbSeekHome._xErr OR fbSetPosAxisV.Error;
	IF bErr THEN
		fbSeekHome(_xHome := FALSE,_xAbort:=TRUE,_Axis := AxisM);
		iStatus := 100;	
	END_IF
	3:
	
	100: // 紧急停止状态
	// 使用FB_DualAxisEmergencyStop进行双轴紧急停止
	fbDualAxisEmergencyStop(
		AxisM := AxisM,
		AxisS := AxisS,
		bExecute := TRUE,
		rDeceleration := 36000
	);
	
	IF fbDualAxisEmergencyStop.bDone THEN
		fbDualAxisEmergencyStop(bExecute := FALSE);
		iStatus := 0; // 返回空闲状态
	END_IF
	
	END_CASE
END_IF

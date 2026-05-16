FUNCTION_BLOCK FB_TripleAxisStop
VAR_INPUT
	AxisX			:	SM3_Basic.AXIS_REF_SM3			//X轴引用
	AxisY			:	SM3_Basic.AXIS_REF_SM3			//Y轴引用
	AxisZ			:	SM3_Basic.AXIS_REF_SM3			//Z轴引用
	bExecute		:	BOOL;				//执行停止信号
	rDeceleration	:	REAL := 100.0;		//减速度
END_VAR
VAR_OUTPUT
	bDone			:	BOOL;				//三轴都停止完成
	bBusy			:	BOOL;				//停止进行中
	bError			:	BOOL;				//错误标志
	sErrorString	:	STRING;				//错误信息字符串
END_VAR
VAR
	fbStopX			:	MC_STOP;			//X轴停止
	fbStopY			:	MC_STOP;			//Y轴停止
	fbStopZ			:	MC_STOP;			//Z轴停止
END_VAR

// X轴停止
fbStopX(
	Execute := bExecute,
	Deceleration := rDeceleration,
	Axis := AxisX
);

// Y轴停止
fbStopY(
	Execute := bExecute,
	Deceleration := rDeceleration,
	Axis := AxisY
);

// Z轴停止
fbStopZ(
	Execute := bExecute,
	Deceleration := rDeceleration,
	Axis := AxisZ
);

// 更新输出状态
bBusy := fbStopX.Busy OR fbStopY.Busy OR fbStopZ.Busy;
bDone := fbStopX.Done AND fbStopY.Done AND fbStopZ.Done;

// 错误检查（优先级：X > Y > Z）
IF fbStopX.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbStopX.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSIF fbStopY.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbStopY.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSIF fbStopZ.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbStopZ.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSE
	bError := FALSE;
	sErrorString := 'CNC_NO_ERROR';
END_IF


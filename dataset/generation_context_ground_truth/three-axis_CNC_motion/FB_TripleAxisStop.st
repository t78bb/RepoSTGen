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


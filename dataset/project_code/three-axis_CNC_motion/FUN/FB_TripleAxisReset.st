FUNCTION_BLOCK FB_TripleAxisReset
VAR_INPUT
	AxisX			:	SM3_Basic.AXIS_REF_SM3			//X轴引用
	AxisY			:	SM3_Basic.AXIS_REF_SM3			//Y轴引用
	AxisZ			:	SM3_Basic.AXIS_REF_SM3			//Z轴引用
	bExecute		:	BOOL;				//执行复位信号
END_VAR
VAR_OUTPUT
	bDone			:	BOOL;				//三轴都复位完成
	bBusy			:	BOOL;				//复位进行中
	bError			:	BOOL;				//错误标志
	sErrorString	:	STRING;				//错误信息字符串
END_VAR
VAR
	fbResetX		:	MC_RESET;			//X轴复位
	fbResetY		:	MC_RESET;			//Y轴复位
	fbResetZ		:	MC_RESET;			//Z轴复位
END_VAR

// X轴复位
fbResetX(
	Execute := bExecute,
	Axis := AxisX
);

// Y轴复位
fbResetY(
	Execute := bExecute,
	Axis := AxisY
);

// Z轴复位
fbResetZ(
	Execute := bExecute,
	Axis := AxisZ
);

// 更新输出状态
bBusy := fbResetX.Busy OR fbResetY.Busy OR fbResetZ.Busy;
bDone := fbResetX.Done AND fbResetY.Done AND fbResetZ.Done;

// 错误检查（优先级：X > Y > Z）
IF fbResetX.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbResetX.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSIF fbResetY.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbResetY.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSIF fbResetZ.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbResetZ.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSE
	bError := FALSE;
	sErrorString := 'CNC_NO_ERROR';
END_IF


VAR
	fbHomingX			:	SMC_HOMING;			//X轴回零功能块
	fbHomingY			:	SMC_HOMING;			//Y轴回零功能块
	fbHomingZ			:	SMC_HOMING;			//Z轴回零功能块
	fbDoneXTrig			:	R_TRIG;				//X轴完成上升沿
	fbDoneYTrig			:	R_TRIG;				//Y轴完成上升沿
	fbDoneZTrig			:	R_TRIG;				//Z轴完成上升沿
END_VAR

// X轴回零
fbHomingX(
	bExecute := bExecute,
	bReferenceSwitch := bAxisXRefSwitch,
	fVelocitySlow := fVelocitySlow,
	fVelocityFast := fVelocityFast,
	fAcceleration := fAcceleration,
	fDeceleration := fDeceleration,
	Axis := AxisX
);

// Y轴回零
fbHomingY(
	bExecute := bExecute,
	bReferenceSwitch := bAxisYRefSwitch,
	fVelocitySlow := fVelocitySlow,
	fVelocityFast := fVelocityFast,
	fAcceleration := fAcceleration,
	fDeceleration := fDeceleration,
	Axis := AxisY
);

// Z轴回零
fbHomingZ(
	bExecute := bExecute,
	bReferenceSwitch := bAxisZRefSwitch,
	fVelocitySlow := fVelocitySlow,
	fVelocityFast := fVelocityFast,
	fAcceleration := fAcceleration,
	fDeceleration := fDeceleration,
	Axis := AxisZ
);

// 检测X轴完成
fbDoneXTrig(CLK := fbHomingX.bDone);
IF fbDoneXTrig.Q THEN
	bAxisXHomeOK := TRUE;
END_IF

// 检测Y轴完成
fbDoneYTrig(CLK := fbHomingY.bDone);
IF fbDoneYTrig.Q THEN
	bAxisYHomeOK := TRUE;
END_IF

// 检测Z轴完成
fbDoneZTrig(CLK := fbHomingZ.bDone);
IF fbDoneZTrig.Q THEN
	bAxisZHomeOK := TRUE;
END_IF

// 更新输出状态
bHomeOK := bAxisXHomeOK AND bAxisYHomeOK AND bAxisZHomeOK;
bBusy := fbHomingX.bBusy OR fbHomingY.bBusy OR fbHomingZ.bBusy;

// 错误检查（优先级：X > Y > Z）
IF fbHomingX.bError THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbHomingX.nErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSIF fbHomingY.bError THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbHomingY.nErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSIF fbHomingZ.bError THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbHomingZ.nErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSE
	bError := FALSE;
	sErrorString := 'CNC_NO_ERROR';
END_IF

// 复位逻辑
IF NOT bExecute THEN
	bAxisXHomeOK := FALSE;
	bAxisYHomeOK := FALSE;
	bAxisZHomeOK := FALSE;
	bHomeOK := FALSE;
END_IF


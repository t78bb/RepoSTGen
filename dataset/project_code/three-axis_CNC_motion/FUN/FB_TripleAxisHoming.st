FUNCTION_BLOCK FB_TripleAxisHoming
VAR_INPUT
	bExecute			:	BOOL;				//执行回零信号
	AxisX				:	SM3_Basic.AXIS_REF_SM3;			//X轴引用
	AxisY				:	SM3_Basic.AXIS_REF_SM3;			//Y轴引用
	AxisZ				:	SM3_Basic.AXIS_REF_SM3;			//Z轴引用
	bAxisXRefSwitch		:	BOOL;				//X轴零点开关
	bAxisYRefSwitch		:	BOOL;				//Y轴零点开关
	bAxisZRefSwitch		:	BOOL;				//Z轴零点开关
	fVelocitySlow		:	REAL;				//慢速回零速度
	fVelocityFast		:	REAL;				//快速回零速度
	fAcceleration		:	REAL;				//加速度
	fDeceleration		:	REAL;				//减速度
END_VAR
VAR_OUTPUT
	bHomeOK				:	BOOL;				//三轴都回零完成
	bAxisXHomeOK		:	BOOL;				//X轴回零完成
	bAxisYHomeOK		:	BOOL;				//Y轴回零完成
	bAxisZHomeOK		:	BOOL;				//Z轴回零完成
	bBusy				:	BOOL;				//回零进行中
	bError				:	BOOL;				//错误标志
	sErrorString		:	STRING;				//错误信息字符串
END_VAR
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


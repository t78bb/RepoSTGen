FUNCTION_BLOCK FB_TripleAxisPower
VAR_INPUT
	AxisX			:	SM3_Basic.AXIS_REF_SM3			//X轴引用
	AxisY			:	SM3_Basic.AXIS_REF_SM3			//Y轴引用
	AxisZ			:	SM3_Basic.AXIS_REF_SM3			//Z轴引用
	bServoEnable	:	BOOL;				//伺服使能信号
END_VAR
VAR_OUTPUT
	bReady			:	BOOL;				//三轴都准备就绪
	bAxisXReady		:	BOOL;				//X轴准备就绪
	bAxisYReady		:	BOOL;				//Y轴准备就绪
	bAxisZReady		:	BOOL;				//Z轴准备就绪
	bError			:	BOOL;				//错误标志
	sErrorString	:	STRING;				//错误信息字符串
END_VAR
VAR
	fbPowerX		:	MC_POWER;			//X轴电源控制
	fbPowerY		:	MC_POWER;			//Y轴电源控制
	fbPowerZ		:	MC_POWER;			//Z轴电源控制
END_VAR

// X轴电源控制
fbPowerX(
	Enable := bServoEnable,
	bRegulatorOn := bServoEnable,
	bDriveStart := bServoEnable,
	Axis := AxisX
);

// Y轴电源控制
fbPowerY(
	Enable := bServoEnable,
	bRegulatorOn := bServoEnable,
	bDriveStart := bServoEnable,
	Axis := AxisY
);

// Z轴电源控制
fbPowerZ(
	Enable := bServoEnable,
	bRegulatorOn := bServoEnable,
	bDriveStart := bServoEnable,
	Axis := AxisZ
);

// 更新输出状态
bAxisXReady := fbPowerX.Status;
bAxisYReady := fbPowerY.Status;
bAxisZReady := fbPowerZ.Status;
bReady := fbPowerX.Status AND fbPowerY.Status AND fbPowerZ.Status;

// 错误检查（优先级：X > Y > Z）
IF fbPowerX.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbPowerX.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSIF fbPowerY.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbPowerY.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSIF fbPowerZ.Error THEN
	bError := TRUE;
	SMC_ERRORSTRING(ErrorID := fbPowerZ.ErrorID, Language := english, SMC_ErrorString => sErrorString);
ELSE
	bError := FALSE;
	sErrorString := 'CNC_NO_ERROR';
END_IF


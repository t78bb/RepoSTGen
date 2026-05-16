FUNCTION_BLOCK FB_DualAxisPower
VAR_IN_OUT
	AxisM		:	AXIS_REF_SM3;		// 主轴引用
	AxisS		:	AXIS_REF_SM3;		// 从轴引用
END_VAR
VAR_INPUT
	bPowerOn	:	BOOL;				// 电源使能信号
END_VAR
VAR_OUTPUT
	bReady		:	BOOL;				// 两轴都准备就绪
	bAxisMReady	:	BOOL;				// 主轴准备状态
	bAxisSReady	:	BOOL;				// 从轴准备状态
	bError		:	BOOL;				// 错误标志
END_VAR
VAR
	fbPowerM	:	SM3_Basic.MC_Power;	// 主轴电源控制
	fbPowerS	:	SM3_Basic.MC_Power;	// 从轴电源控制
END_VAR

// 主轴电源控制
fbPowerM(
	Axis := AxisM,
	Enable := TRUE,
	bRegulatorOn := bPowerOn,
	bDriveStart := bPowerOn
);

// 从轴电源控制
fbPowerS(
	Axis := AxisS,
	Enable := TRUE,
	bRegulatorOn := bPowerOn,
	bDriveStart := bPowerOn
);

// 更新输出状态
bAxisMReady := fbPowerM.Status;
bAxisSReady := fbPowerS.Status;
bReady := fbPowerM.Status AND fbPowerS.Status;

// 错误处理
bError := fbPowerM.Error OR fbPowerS.Error;


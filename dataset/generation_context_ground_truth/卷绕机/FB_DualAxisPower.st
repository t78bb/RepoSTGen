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


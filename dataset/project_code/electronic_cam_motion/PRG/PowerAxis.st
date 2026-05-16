PROGRAM PowerAxis
VAR
	fbDualPower		:	FB_DualAxisPower;	//双轴电源控制功能块
	bPowerOn		:	BOOL;
END_VAR
VAR_OUTPUT 
	bPowerDone		:	BOOL;
END_VAR

// 使用双轴电源控制功能块
fbDualPower(
	Axis1 := AxisX,
	Axis2 := AxisY,
	bPowerOn := bPowerOn
);

// 输出状态
bPowerDone := fbDualPower.bPowerDone;

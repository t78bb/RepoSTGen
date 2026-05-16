FUNCTION_BLOCK FB_DualAxisPower
VAR_INPUT
	Axis1			:	AXIS_REF;		//轴1引用
	Axis2			:	AXIS_REF;		//轴2引用
	bEnable			:	BOOL := TRUE;	//使能信号
END_VAR
VAR_OUTPUT
	bAxis1Ready		:	BOOL;			//轴1准备就绪
	bAxis2Ready		:	BOOL;			//轴2准备就绪
	bBothReady		:	BOOL;			//两轴都准备就绪
	bError			:	BOOL;			//错误标志
END_VAR
VAR
	fbPower1		:	MC_Power;		//轴1电源控制
	fbPower2		:	MC_Power;		//轴2电源控制
END_VAR

// 执行轴1电源控制
fbPower1(
	Axis := Axis1,
	Enable := bEnable,
	bDriveStart := TRUE,
	bRegulatorOn := TRUE
);

// 执行轴2电源控制
fbPower2(
	Axis := Axis2,
	Enable := bEnable,
	bDriveStart := TRUE,
	bRegulatorOn := TRUE
);

// 更新输出状态
bAxis1Ready := fbPower1.Status;
bAxis2Ready := fbPower2.Status;
bBothReady := fbPower1.Status AND fbPower2.Status;
bError := fbPower1.Error OR fbPower2.Error;


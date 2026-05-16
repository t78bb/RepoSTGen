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


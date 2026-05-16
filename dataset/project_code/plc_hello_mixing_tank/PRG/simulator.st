PROGRAM simulator
VAR
	///模拟混合电机
	MixerMotor				:	GenericBistableDeviceModel;
	///模拟介质1填充阀门
	MediumValve1			:	GenericBistableDeviceModel;
	///模拟介质2填充阀门
	MediumValve2			:	GenericBistableDeviceModel;
	///模拟排空阀门
	DrainValve				:	GenericBistableDeviceModel;
	
	///液位模拟器
	fbTankLevelSimulator	:	FB_TankLevelSimulator;
	
	///当前液位
	vTankLevel				:	REAL;
	///电机旋转角度（HMI用）
	vMotorRotating			:	REAL;
END_VAR

// ========== 电机和阀门模拟 ==========
MixerMotor(
	ActivateCmd := IO.xDO_M1_MixerMotorRunCmd,
	DeactivateCmd := NOT IO.xDO_M1_MixerMotorRunCmd,
	cfgActTime := T#2S,
	cfgDeactTime := T#0S,
	Activated => IO.xDI_M1_MixerMotorRunning
);

MediumValve1(
	ActivateCmd := IO.xDO_VV01_Medium1_OpenCmd,
	DeactivateCmd := NOT IO.xDO_VV01_Medium1_OpenCmd,
	cfgActTime := T#1S,
	cfgDeactTime := T#1S,
	Activated => IO.xDI_VV01_Medium1_Opened
);

MediumValve2(
	ActivateCmd := IO.xDO_VV02_Medium2_OpenCmd,
	DeactivateCmd := NOT IO.xDO_VV02_Medium2_OpenCmd,
	cfgActTime := T#1S,
	cfgDeactTime := T#1S,
	Activated => IO.xDI_VV02_Medium2_Opened
);

DrainValve(
	ActivateCmd := IO.xDO_VV03_TankDrain_OpenCmd,
	DeactivateCmd := NOT IO.xDO_VV03_TankDrain_OpenCmd,
	cfgActTime := T#1S,
	cfgDeactTime := T#1S,
	Activated => IO.xDI_VV03_TankDrain_Opened
);

// ========== 液位模拟 ==========
fbTankLevelSimulator(
	bMedium1Opened := MediumValve1.Activated,
	bMedium2Opened := MediumValve2.Activated,
	bDrainOpened := DrainValve.Activated,
	bReset := FALSE,
	rInitialLevel := 25.0,
	rFillRate1 := 0.1,
	rFillRate2 := 0.1,
	rDrainRate := 0.2,
	rMinLevel := 0.0,
	rMaxLevel := 100.0
);
vTankLevel := fbTankLevelSimulator.rCurrentLevel;

// ========== 液位开关模拟 ==========
F_UpdateLimitSwitches(
	rTankLevel := vTankLevel,
	rFullThreshold := 85.0,
	rEmptyThreshold := 5.0,
	bLevelFull => IO.xDI_LS01_TankLevelFull,
	bLevelEmpty => IO.xDI_LS02_TankLevelEmpty
);

// ========== HMI 电机旋转动画 ==========
vMotorRotating := vMotorRotating + 1 * BOOL_TO_REAL(MixerMotor.Activated);
IF vMotorRotating >= 360 THEN 
	vMotorRotating := 0; 
END_IF

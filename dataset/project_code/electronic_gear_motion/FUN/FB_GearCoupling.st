FUNCTION_BLOCK FB_GearCoupling
VAR_INPUT
	Master				:	AXIS_REF;		//主轴引用
	Slave				:	AXIS_REF;		//从轴引用
	bCouple				:	BOOL;			//TRUE=耦合，FALSE=解耦
	nRatioNumerator		:	INT := 1;		//传动比分子
	nRatioDenominator	:	INT := 1;		//传动比分母
	rAcceleration		:	REAL := 10000.0;//加速度
	rDeceleration		:	REAL := 10000.0;//减速度
END_VAR
VAR_OUTPUT
	bInGear				:	BOOL;			//耦合状态
	bCouplingDone		:	BOOL;			//耦合完成
	bDecouplingDone		:	BOOL;			//解耦完成
	bError				:	BOOL;			//错误标志
	nErrorID			:	DWORD;			//错误代码
END_VAR
VAR
	fbGearIn			:	MC_GearIn;		//齿轮耦合功能块
	fbGearOut			:	MC_GearOut;		//齿轮解耦功能块
	bLastCouple			:	BOOL;			//上次耦合状态
	bCoupleRising		:	BOOL;			//耦合上升沿
	bCoupleFalling		:	BOOL;			//耦合下降沿
END_VAR

// 检测耦合信号的边沿
bCoupleRising := bCouple AND NOT bLastCouple;
bCoupleFalling := NOT bCouple AND bLastCouple;
bLastCouple := bCouple;

// 齿轮耦合控制
IF bCouple THEN
	// 执行耦合
	fbGearIn(
		Execute := TRUE,
		Master := Master,
		Slave := Slave,
		RatioNumerator := nRatioNumerator,
		RatioDenominator := nRatioDenominator,
		Acceleration := rAcceleration,
		Deceleration := rDeceleration
	);
	
	bInGear := fbGearIn.InGear;
	bCouplingDone := fbGearIn.InGear;
	bDecouplingDone := FALSE;
	bError := fbGearIn.Error;
	nErrorID := fbGearIn.ErrorID;
ELSE
	// 执行解耦
	fbGearIn(Execute := FALSE, Master := Master, Slave := Slave);
	
	fbGearOut(
		Execute := TRUE,
		Slave := Slave
	);
	
	bInGear := FALSE;
	bCouplingDone := FALSE;
	bDecouplingDone := fbGearOut.Done;
	bError := fbGearOut.Error;
	nErrorID := fbGearOut.ErrorID;
	
	// 解耦完成后复位
	IF fbGearOut.Done THEN
		fbGearOut(Execute := FALSE, Slave := Slave);
	END_IF
END_IF


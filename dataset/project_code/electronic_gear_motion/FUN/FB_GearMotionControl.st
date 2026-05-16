FUNCTION_BLOCK FB_GearMotionControl
VAR_INPUT
	MasterAxis			:	AXIS_REF;		//主轴引用
	SlaveAxis			:	AXIS_REF;		//从轴引用
	bStart				:	BOOL;			//启动信号
	bStop				:	BOOL;			//停止信号
	nRatioNumerator		:	INT := 1;		//传动比分子
	nRatioDenominator	:	INT := 1;		//传动比分母
	nDirection			:	INT := 1;		//运动方向（1=正向，-1=反向）
	rVelocity			:	REAL := 360.0;	//主轴速度
	rAcceleration		:	REAL := 10000.0;//加速度
	rDeceleration		:	REAL := 10000.0;//减速度
END_VAR
VAR_OUTPUT
	bRunning			:	BOOL;			//运行中
	bReady				:	BOOL;			//准备就绪（可以启动）
	bError				:	BOOL;			//错误标志
	nCurrentState		:	BYTE;			//当前状态
END_VAR
VAR
	fbPowerMgr			:	FB_DualAxisPower;	//双轴电源管理
	fbGearCtrl			:	FB_GearCoupling;	//齿轮耦合控制
	fbMoveVel			:	MC_MoveVelocity;	//速度运动
	fbHaltMaster		:	MC_Halt;			//主轴停止
	fbHaltSlave			:	MC_Halt;			//从轴停止
	fbStartRtrig		:	R_TRIG;				//启动上升沿
	fbStopRtrig			:	R_TRIG;				//停止上升沿
	nState				:	BYTE;				//内部状态机
END_VAR

// 双轴电源管理
fbPowerMgr(
	Axis1 := MasterAxis,
	Axis2 := SlaveAxis,
	bEnable := TRUE
);

// 状态机
CASE nState OF
	0: (* 等待轴准备就绪 *)
		bRunning := FALSE;
		bReady := FALSE;
		IF fbPowerMgr.bBothReady THEN
			nState := 1;
			bReady := TRUE;
		END_IF
		
	1: (* 等待启动信号 *)
		bRunning := FALSE;
		bReady := TRUE;
		fbStartRtrig(CLK := bStart);
		IF fbStartRtrig.Q THEN
			nState := 2;
			// 初始化复位
			fbGearCtrl.bCouple := FALSE;
			fbMoveVel(Execute := FALSE, Axis := MasterAxis);
		END_IF
		
	2: (* 执行齿轮耦合和运动 *)
		bRunning := TRUE;
		bReady := FALSE;
		
		// 启动齿轮耦合
		fbGearCtrl(
			Master := MasterAxis,
			Slave := SlaveAxis,
			bCouple := TRUE,
			nRatioNumerator := nRatioNumerator,
			nRatioDenominator := nRatioDenominator,
			rAcceleration := rAcceleration,
			rDeceleration := rDeceleration
		);
		
		// 主轴执行速度运动
		fbMoveVel(
			Execute := fbGearCtrl.bInGear,
			Direction := nDirection,
			Velocity := rVelocity,
			Acceleration := rAcceleration,
			Deceleration := rDeceleration,
			Axis := MasterAxis
		);
		
		// 检测停止信号
		fbStopRtrig(CLK := bStop);
		IF fbStopRtrig.Q THEN
			nState := 3;
			fbMoveVel(Execute := FALSE, Axis := MasterAxis);
			fbHaltMaster(Axis := MasterAxis, Execute := FALSE);
		END_IF
		
	3: (* 停止主轴 *)
		bRunning := FALSE;
		
		// 解除齿轮耦合
		fbGearCtrl(
			Master := MasterAxis,
			Slave := SlaveAxis,
			bCouple := FALSE
		);
		
		// 停止主轴
		fbHaltMaster(
			Axis := MasterAxis,
			Execute := TRUE,
			Deceleration := rDeceleration
		);
		
		IF fbHaltMaster.Done THEN
			fbHaltMaster(Axis := MasterAxis, Execute := FALSE);
			fbHaltSlave(Axis := SlaveAxis, Execute := FALSE);
			nState := 4;
		END_IF
		
	4: (* 停止从轴 *)
		// 等待解耦完成
		IF fbGearCtrl.bDecouplingDone THEN
			fbHaltSlave(
				Axis := SlaveAxis,
				Execute := TRUE,
				Deceleration := rDeceleration
			);
			
			IF fbHaltSlave.Done THEN
				fbHaltSlave(Axis := SlaveAxis, Execute := FALSE);
				nState := 1;  // 返回等待启动状态
			END_IF
		END_IF
END_CASE

// 更新输出
nCurrentState := nState;
bError := fbPowerMgr.bError OR fbGearCtrl.bError OR fbMoveVel.Error OR fbHaltMaster.Error OR fbHaltSlave.Error;


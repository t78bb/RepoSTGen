PROGRAM PLC_PRG
VAR
	(* 使用重构后的齿轮运动控制FB *)
	fbGearMotion	:	FB_GearMotionControl;
	
	(* 用户接口 *)
	bStart			:	BOOL;	(* 齿轮联动启动 *)
	bStop			:	BOOL;	(* 齿轮联动停止 *)
	
	(* 运动参数配置 *)
	nGearRatioNum	:	INT := 1;		(* 齿轮比分子 *)
	nGearRatioDen	:	INT := 1;		(* 齿轮比分母 *)
	rMasterVel		:	REAL := 360.0;	(* 主轴速度 *)
	rAccel			:	REAL := 10000.0;(* 加速度 *)
	rDecel			:	REAL := 10000.0;(* 减速度 *)
	
	(* 状态监控 *)
	bSystemReady	:	BOOL;	(* 系统准备就绪 *)
	bSystemRunning	:	BOOL;	(* 系统运行中 *)
	bSystemError	:	BOOL;	(* 系统错误 *)
	nSystemState	:	BYTE;	(* 系统当前状态 *)
END_VAR

(* ========== 齿轮运动控制 ========== *)
fbGearMotion(
	MasterAxis := Axis1,
	SlaveAxis := Axis2,
	bStart := bStart,
	bStop := bStop,
	nRatioNumerator := nGearRatioNum,
	nRatioDenominator := nGearRatioDen,
	nDirection := 1,
	rVelocity := rMasterVel,
	rAcceleration := rAccel,
	rDeceleration := rDecel
);

(* 状态监控输出 *)
bSystemReady := fbGearMotion.bReady;
bSystemRunning := fbGearMotion.bRunning;
bSystemError := fbGearMotion.bError;
nSystemState := fbGearMotion.nCurrentState;

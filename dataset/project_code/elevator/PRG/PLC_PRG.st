PROGRAM PLC_PRG
VAR
	// 输入信号
	CallGround, CallFloor1, CallFloor2, CallFloor3: BOOL;
	FloorSensor0, FloorSensor1, FloorSensor2, FloorSensor3: BOOL;
	DoorClosed: BOOL;
	EmergencyStop: BOOL;

	// 输出信号
	OpenDoor: BOOL := FALSE;
	CloseDoor: BOOL := FALSE;

	// 内部变量
	TargetFloors: ARRAY[0..3] OF BOOL := [FALSE, FALSE, FALSE, FALSE];
	CurrentFloor: INT := 0;
	
	// 使用重构后的功能块
	fbDoorController		:	FB_ElevatorDoorController;		// 门控制器
	fbMovementController	:	FB_ElevatorMovement;			// 移动控制器
	
	// 门开关动画
	aniDoor0, aniDoor1, aniDoor2, aniDoor3: DINT := 0;
END_VAR

// ========== 紧急停止处理 ==========
IF EmergencyStop THEN
	OpenDoor := FALSE;
	CloseDoor := FALSE;
	// 复位功能块
	fbDoorController(bArrivedAtTarget := FALSE, bDoorClosed := DoorClosed);
	fbMovementController(CurrentFloor := CurrentFloor, bDoorReady := FALSE, TargetFloors := TargetFloors);
	RETURN;
END_IF

// ========== 楼层检测 ==========
CurrentFloor := F_DetectCurrentFloor(
	FloorSensor0 := FloorSensor0,
	FloorSensor1 := FloorSensor1,
	FloorSensor2 := FloorSensor2,
	FloorSensor3 := FloorSensor3,
	CurrentFloor := CurrentFloor
);

// ========== 呼叫注册 ==========
F_RegisterCalls(
	CallGround := CallGround,
	CallFloor1 := CallFloor1,
	CallFloor2 := CallFloor2,
	CallFloor3 := CallFloor3,
	TargetFloors := TargetFloors
);

// ========== 电梯移动控制 ==========
fbMovementController(
	CurrentFloor := CurrentFloor,
	bDoorReady := fbDoorController.bDoorReady,
	TargetFloors := TargetFloors
);

// ========== 门控制 ==========
fbDoorController(
	bArrivedAtTarget := fbMovementController.bArrivedAtTarget,
	bDoorClosed := DoorClosed
);

// 更新输出
OpenDoor := fbDoorController.bOpenDoor;
CloseDoor := fbDoorController.bCloseDoor;

// ========== 门动画更新 ==========
aniDoor0 := F_UpdateDoorAnimation(
	bOpenDoor := OpenDoor,
	bCloseDoor := CloseDoor,
	bCallFloor := CallGround,
	nCurrentAni := aniDoor0,
	nMaxAni := 70
);

aniDoor1 := F_UpdateDoorAnimation(
	bOpenDoor := OpenDoor,
	bCloseDoor := CloseDoor,
	bCallFloor := CallFloor1,
	nCurrentAni := aniDoor1,
	nMaxAni := 70
);

aniDoor2 := F_UpdateDoorAnimation(
	bOpenDoor := OpenDoor,
	bCloseDoor := CloseDoor,
	bCallFloor := CallFloor2,
	nCurrentAni := aniDoor2,
	nMaxAni := 70
);

aniDoor3 := F_UpdateDoorAnimation(
	bOpenDoor := OpenDoor,
	bCloseDoor := CloseDoor,
	bCallFloor := CallFloor3,
	nCurrentAni := aniDoor3,
	nMaxAni := 70
);

// End Program...

FUNCTION F_DetectCurrentFloor : INT
VAR_INPUT
	FloorSensor0	:	BOOL;		// 0楼传感器
	FloorSensor1	:	BOOL;		// 1楼传感器
	FloorSensor2	:	BOOL;		// 2楼传感器
	FloorSensor3	:	BOOL;		// 3楼传感器
	CurrentFloor	:	INT;		// 当前楼层（用于保持状态）
END_VAR

// 根据传感器输入确定当前楼层
IF FloorSensor0 THEN 
	F_DetectCurrentFloor := 0;
ELSIF FloorSensor1 THEN 
	F_DetectCurrentFloor := 1;
ELSIF FloorSensor2 THEN 
	F_DetectCurrentFloor := 2;
ELSIF FloorSensor3 THEN 
	F_DetectCurrentFloor := 3;
ELSE
	// 没有传感器信号时，保持当前楼层
	F_DetectCurrentFloor := CurrentFloor;
END_IF


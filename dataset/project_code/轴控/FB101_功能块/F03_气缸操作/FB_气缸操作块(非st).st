FUNCTION_BLOCK FB_气缸操作块
VAR_INPUT
	CheckTime: TIME := T#3S;
	OpenSensor: BOOL;
	CloseSensor: BOOL;
	
	OpenSensorCheck: BOOL;
	CloseSensorCheck: BOOL;
	
	OpenDelayTime: REAL;
	CloseDelayTime: REAL;
	
	Cylinder: BOOL;
END_VAR


VAR_OUTPUT
	Q_CylinderError1: BOOL;
	Q_CylinderError2: BOOL;
	OpenDelay: BOOL;
	CloseDelay: BOOL;
END_VAR
VAR
	Delay1: TON;
	Delay2: TON;
	TON0: TON;
	TON1: TON;
END_VAR

// -----------------------------------------------------
// 网络 1: 气缸打开超时错误 (Q_CylinderError1)
// -----------------------------------------------------
// 逻辑: (Cylinder AND NOT OpenSensorCheck) 启动定时器 Delay1。
// 定时器 PT 为 CheckTime。当 OpenSensorCheck 变为 TRUE 时，定时器复位。
// 错误条件: (定时器 Q 输出为 TRUE) AND (CloseSensorCheck 为 TRUE)。
// 气缸在动作（Cylinder为TRUE）且要求打开但没有在位（OpenSensorCheck为FALSE）时开始计时。
// 如果超时（Delay1.Q）且气缸仍处于关闭状态的传感器检测（CloseSensorCheck为TRUE），则报错。

Delay1(
    IN := Cylinder AND NOT OpenSensorCheck, // 定时器 IN 信号
    PT := CheckTime,                       // 预设时间
    Q  => ,                                // Q 输出在 TON 实例中不需要连接到临时变量
    ET =>                                  // ET 输出通常不连
);

Q_CylinderError1 := Delay1.Q AND CloseSensorCheck;


// -----------------------------------------------------
// 网络 2: 气缸关闭超时错误 (Q_CylinderError2)
// -----------------------------------------------------
// 逻辑: (NOT Cylinder AND NOT CloseSensorCheck) 启动定时器 Delay2。
// 定时器 PT 为 CheckTime。当 CloseSensorCheck 变为 TRUE 时，定时器复位。
// 错误条件: (定时器 Q 输出为 TRUE) AND (OpenSensorCheck 为 TRUE)。
// 气缸在动作（Cylinder为FALSE）且要求关闭但没有在位（CloseSensorCheck为FALSE）时开始计时。
// 如果超时（Delay2.Q）且气缸仍处于打开状态的传感器检测（OpenSensorCheck为TRUE），则报错。

Delay2(
    IN := NOT Cylinder AND NOT CloseSensorCheck, // 定时器 IN 信号
    PT := CheckTime,                            // 预设时间
    Q  => ,                                     // Q 输出在 TON 实例中不需要连接到临时变量
    ET => 
);

Q_CylinderError2 := Delay2.Q AND OpenSensorCheck;


// -----------------------------------------------------
// 网络 3: 打开延时 (OpenDelay)
// -----------------------------------------------------
// 逻辑: 气缸打开到位检测（OpenSensorCheck AND NOT CloseSensorCheck）触发 TON0 计时。
// PT 由 REAL_TO_TIME(OpenDelayTime * 1000) 设定。
// 延时输出 (OpenDelay) 为 TON0 的 Q 输出。

TON0(
    IN := OpenSensorCheck AND NOT CloseSensorCheck, // 气缸开到位且不在关到位
    PT := REAL_TO_TIME(OpenDelayTime * 1000.0),     // REAL_TO_TIME 函数将 REAL 秒数转换为 TIME 毫秒
    Q  => OpenDelay,                                // Q 输出连接到 OpenDelay
    ET => 
);


// -----------------------------------------------------
// 网络 4: 关闭延时 (CloseDelay)
// -----------------------------------------------------
// 逻辑: 气缸关闭到位检测（CloseSensorCheck AND NOT OpenSensorCheck）触发 TON1 计时。
// PT 由 REAL_TO_TIME(CloseDelayTime * 1000) 设定。
// 延时输出 (CloseDelay) 为 TON1 的 Q 输出。

TON1(
    IN := CloseSensorCheck AND NOT OpenSensorCheck, // 气缸关到位且不在开到位
    PT := REAL_TO_TIME(CloseDelayTime * 1000.0),    // REAL_TO_TIME 函数将 REAL 秒数转换为 TIME 毫秒
    Q  => CloseDelay,                               // Q 输出连接到 CloseDelay
    ET => 
);
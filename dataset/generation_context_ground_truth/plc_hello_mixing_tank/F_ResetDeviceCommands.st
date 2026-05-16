
// 命令合理性复位
// 当设备到达目标状态时，复位相应的命令标志

// 混合电机命令复位
IF bMixerRunning THEN
	bMixerRunCmd := FALSE;		// 已运行，复位运行命令
ELSE
	bMixerStopCmd := FALSE;		// 已停止，复位停止命令
END_IF

// 介质1阀门命令复位
IF bMedium1Opened THEN
	bMedium1OpenCmd := FALSE;	// 已打开，复位打开命令
ELSE
	bMedium1CloseCmd := FALSE;	// 已关闭，复位关闭命令
END_IF

// 介质2阀门命令复位
IF bMedium2Opened THEN
	bMedium2OpenCmd := FALSE;	// 已打开，复位打开命令
ELSE
	bMedium2CloseCmd := FALSE;	// 已关闭，复位关闭命令
END_IF

// 排空阀门命令复位
IF bDrainOpened THEN
	bDrainOpenCmd := FALSE;		// 已打开，复位打开命令
ELSE
	bDrainCloseCmd := FALSE;	// 已关闭，复位关闭命令
END_IF

F_ResetDeviceCommands := TRUE;


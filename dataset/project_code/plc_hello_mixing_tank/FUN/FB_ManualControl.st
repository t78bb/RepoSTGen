FUNCTION_BLOCK FB_ManualControl
VAR_INPUT
	// HMI命令输入
	bMixerRunCmd		:	BOOL;
	bMixerStopCmd		:	BOOL;
	bMedium1OpenCmd		:	BOOL;
	bMedium1CloseCmd	:	BOOL;
	bMedium2OpenCmd		:	BOOL;
	bMedium2CloseCmd	:	BOOL;
	bDrainOpenCmd		:	BOOL;
	bDrainCloseCmd		:	BOOL;
	
	// 设备反馈输入
	bMixerRunning		:	BOOL;
	bMedium1Opened		:	BOOL;
	bMedium2Opened		:	BOOL;
	bDrainOpened		:	BOOL;
END_VAR
VAR_OUTPUT
	// 设备控制输出
	bMixerRunCmdOut		:	BOOL;
	bMedium1OpenCmdOut	:	BOOL;
	bMedium2OpenCmdOut	:	BOOL;
	bDrainOpenCmdOut	:	BOOL;
END_VAR

// 手动模式：HMI命令通过锁存器控制设备
// 锁存逻辑：按下启动OR已启动反馈 AND NOT 按下停止

// 混合电机控制
bMixerRunCmdOut := (bMixerRunCmd OR bMixerRunning) AND NOT bMixerStopCmd;

// 介质1阀门控制
bMedium1OpenCmdOut := (bMedium1OpenCmd OR bMedium1Opened) AND NOT bMedium1CloseCmd;

// 介质2阀门控制
bMedium2OpenCmdOut := (bMedium2OpenCmd OR bMedium2Opened) AND NOT bMedium2CloseCmd;

// 排空阀门控制
bDrainOpenCmdOut := (bDrainOpenCmd OR bDrainOpened) AND NOT bDrainCloseCmd;


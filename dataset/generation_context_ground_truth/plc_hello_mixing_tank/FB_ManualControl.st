
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


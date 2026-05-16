PROGRAM main
VAR
	///模式控制器
	fbModeController		:	FB_ModeController;
	///手动控制功能块
	fbManualControl			:	FB_ManualControl;
	///自动序列控制功能块
	fbAutoSequence			:	FB_AutoSequence;
	
	///当前运行模式
	vMode					:	MODES;
END_VAR
(*Functional description:
There are two ways of operation:
	- Manual
	- Automatic
Manual:
	- Operator is able to operate each valve manually
	- Operator is able to operate the mixer motor manually
	- Overfill protections are disabled
	- Operator is able to put the system to auto
	
Automatic:
	- Program will automatically control the valves and the mixing motor if system is in auto
	- If the tanks level is undefined it assumes draining state
	- In draining state, drains the tank until LS02 activates (tank is empty)
	- When tank is empty, it activates the medium 1 and 2 valves, closes the drain valve and the tank is filling up
	- Filling state is until LS01 is activated (Tank is full)
	- Then the mixer motor is mixing for 10 seconds
	- After mixing is completed, drain the whole contents
	- Repeats as long as auto is activated
	
HMI Requirements:
	- Manual / Auto needs to be correctly controlled and displayed
	- If manual, clicking on devices activates or stops them
	- If auto, clicking is not doing anything
	- If auto, system is counting number of cycles completed
	- Devices must clearly display if they are activated or deactivated*)

// ========== 模式控制 ==========
fbModeController(
	bSetToAuto := HMI.SetToAuto,
	bSetToManual := HMI.SetToManual
);
vMode := fbModeController.eCurrentMode;

// 模式切换时，复位HMI命令
IF fbModeController.bModeChanged THEN
	HMI.SetToAuto := FALSE;
	HMI.SetToManual := FALSE;
END_IF

// ========== 控制逻辑 ==========
CASE vMode OF
	MODES.MANUAL: (*手动模式*)
		// 使用手动控制功能块
		fbManualControl(
			bMixerRunCmd := HMI.MixerRunCmd,
			bMixerStopCmd := HMI.MixerStopCmd,
			bMedium1OpenCmd := HMI.Medium1OpenCmd,
			bMedium1CloseCmd := HMI.Medium1CloseCmd,
			bMedium2OpenCmd := HMI.Medium2OpenCmd,
			bMedium2CloseCmd := HMI.Medium2CloseCmd,
			bDrainOpenCmd := HMI.DrainOpenCmd,
			bDrainCloseCmd := HMI.DrainCloseCmd,
			bMixerRunning := IO.xDI_M1_MixerMotorRunning,
			bMedium1Opened := IO.xDI_VV01_Medium1_Opened,
			bMedium2Opened := IO.xDI_VV02_Medium2_Opened,
			bDrainOpened := IO.xDI_VV03_TankDrain_Opened
		);
		
		// 输出到IO
		IO.xDO_M1_MixerMotorRunCmd := fbManualControl.bMixerRunCmdOut;
		IO.xDO_VV01_Medium1_OpenCmd := fbManualControl.bMedium1OpenCmdOut;
		IO.xDO_VV02_Medium2_OpenCmd := fbManualControl.bMedium2OpenCmdOut;
		IO.xDO_VV03_TankDrain_OpenCmd := fbManualControl.bDrainOpenCmdOut;
		
		// 自动序列禁用
		fbAutoSequence(bEnable := FALSE);
	
	MODES.AUTO: (*自动模式*)
		// 使用自动序列功能块
		fbAutoSequence(
			bEnable := TRUE,
			bReset := fbModeController.bModeChanged,
			bTankLevelFull := IO.xDI_LS01_TankLevelFull,
			bTankLevelEmpty := IO.xDI_LS02_TankLevelEmpty,
			bMixerRunning := IO.xDI_M1_MixerMotorRunning,
			bMedium1Opened := IO.xDI_VV01_Medium1_Opened,
			bMedium2Opened := IO.xDI_VV02_Medium2_Opened,
			bDrainOpened := IO.xDI_VV03_TankDrain_Opened,
			tMixingDuration := T#10S
		);
		
		// 输出到IO
		IO.xDO_M1_MixerMotorRunCmd := fbAutoSequence.bMixerRunCmd;
		IO.xDO_VV01_Medium1_OpenCmd := fbAutoSequence.bMedium1OpenCmd;
		IO.xDO_VV02_Medium2_OpenCmd := fbAutoSequence.bMedium2OpenCmd;
		IO.xDO_VV03_TankDrain_OpenCmd := fbAutoSequence.bDrainOpenCmd;
		
		// 更新循环计数
		HMI.CyclesCompleted := fbAutoSequence.nCyclesCompleted;
END_CASE

// ========== HMI命令复位 ==========
F_ResetDeviceCommands(
	bMixerRunCmd := HMI.MixerRunCmd,
	bMixerStopCmd := HMI.MixerStopCmd,
	bMedium1OpenCmd := HMI.Medium1OpenCmd,
	bMedium1CloseCmd := HMI.Medium1CloseCmd,
	bMedium2OpenCmd := HMI.Medium2OpenCmd,
	bMedium2CloseCmd := HMI.Medium2CloseCmd,
	bDrainOpenCmd := HMI.DrainOpenCmd,
	bDrainCloseCmd := HMI.DrainCloseCmd,
	bMixerRunning := IO.xDI_M1_MixerMotorRunning,
	bMedium1Opened := IO.xDI_VV01_Medium1_Opened,
	bMedium2Opened := IO.xDI_VV02_Medium2_Opened,
	bDrainOpened := IO.xDI_VV03_TankDrain_Opened
);

// ========== HMI状态更新 ==========
HMI.MotorRotating := HMI.MotorRotating + 2 * BOOL_TO_REAL(IO.xDI_M1_MixerMotorRunning);
IF HMI.MotorRotating >= 360 THEN 
	HMI.MotorRotating := 0; 
END_IF
HMI.InAuto := vMode = MODES.AUTO;
HMI.InManual := vMode = MODES.MANUAL;

FUNCTION_BLOCK FB_ModeController
VAR_INPUT
	bSetToAuto		:	BOOL;	// 切换到自动模式命令
	bSetToManual	:	BOOL;	// 切换到手动模式命令
END_VAR
VAR_OUTPUT
	eCurrentMode	:	MODES;	// 当前模式
	bModeChanged	:	BOOL;	// 模式改变标志
END_VAR
VAR
	eLastMode		:	MODES;	// 上次模式
END_VAR

// 模式切换逻辑
CASE eCurrentMode OF
	MODES.AUTO:
		IF bSetToManual THEN
			eCurrentMode := MODES.MANUAL;
		END_IF
		
	MODES.MANUAL:
		IF bSetToAuto THEN
			eCurrentMode := MODES.AUTO;
		END_IF
END_CASE

// 检测模式变化
bModeChanged := (eCurrentMode <> eLastMode);
eLastMode := eCurrentMode;


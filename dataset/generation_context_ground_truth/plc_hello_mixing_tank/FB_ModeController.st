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


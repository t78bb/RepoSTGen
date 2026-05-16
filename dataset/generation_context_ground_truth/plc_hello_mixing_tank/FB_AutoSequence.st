VAR
	tonMixing			:	TON;			// 混合定时器
END_VAR

// 复位逻辑
IF bReset THEN
	eCurrentState := AUTO_SEQUENCE.DRAINING;
	nCyclesCompleted := 0;
END_IF

// 自动序列状态机
IF bEnable THEN
	CASE eCurrentState OF
		AUTO_SEQUENCE.FILLING:
			// 确保其他设备不工作
			bMixerRunCmd := FALSE;
			bDrainOpenCmd := FALSE;
			
			// 打开两个介质阀门，开始填充罐体
			bMedium1OpenCmd := NOT bTankLevelFull;
			bMedium2OpenCmd := NOT bTankLevelFull;
			
			// 当罐体满时，等待填充阀关闭，然后进入混合状态
			IF bTankLevelFull AND NOT (bMedium1Opened OR bMedium2Opened) THEN
				eCurrentState := AUTO_SEQUENCE.MIXING;
			END_IF
			
		AUTO_SEQUENCE.MIXING:
			// 确保其他设备不工作
			bMedium1OpenCmd := FALSE;
			bMedium2OpenCmd := FALSE;
			bDrainOpenCmd := FALSE;
			
			// 启动混合电机并混合10秒
			bMixerRunCmd := TRUE;
			tonMixing(IN := bMixerRunning, PT := tMixingDuration);
			
			// 当定时器到达10秒，等待电机停止运行，然后进入排空状态
			IF tonMixing.Q THEN
				bMixerRunCmd := FALSE;
				eCurrentState := AUTO_SEQUENCE.DRAINING;
			END_IF
			
		AUTO_SEQUENCE.DRAINING:
			// 确保其他设备不工作
			bMixerRunCmd := FALSE;
			bMedium1OpenCmd := FALSE;
			bMedium2OpenCmd := FALSE;
			
			// 打开排空阀，开始排空罐体
			bDrainOpenCmd := NOT bTankLevelEmpty;
			
			// 当罐体空时，等待排空阀关闭，然后进入填充状态
			IF bTankLevelEmpty AND NOT bDrainOpened THEN
				eCurrentState := AUTO_SEQUENCE.FILLING;
				nCyclesCompleted := nCyclesCompleted + 1;
			END_IF
	END_CASE
ELSE
	// 禁用时，关闭所有输出
	bMixerRunCmd := FALSE;
	bMedium1OpenCmd := FALSE;
	bMedium2OpenCmd := FALSE;
	bDrainOpenCmd := FALSE;
	tonMixing(IN := FALSE);
END_IF


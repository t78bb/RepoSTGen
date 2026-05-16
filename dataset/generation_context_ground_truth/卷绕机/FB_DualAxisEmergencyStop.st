VAR
	fbHaltM			:	MC_Halt;			// 主轴停止功能块
	fbHaltS			:	MC_Halt;			// 从轴停止功能块
	fbRtrigExecute	:	R_TRIG;				// 执行上升沿检测
	nState			:	BYTE;				// 内部状态机
END_VAR

fbRtrigExecute(CLK := bExecute);

CASE nState OF
	0: // 空闲/初始化
		bDone := FALSE;
		bBusy := FALSE;
		bError := FALSE;
		fbHaltM(Axis := AxisM, Execute := FALSE);
		fbHaltS(Axis := AxisS, Execute := FALSE);
		
		IF fbRtrigExecute.Q THEN
			nState := 1;
			bBusy := TRUE;
		END_IF
		
	1: // 执行双轴停止
		fbHaltM(
			Axis := AxisM,
			Execute := TRUE,
			Deceleration := rDeceleration
		);
		
		fbHaltS(
			Axis := AxisS,
			Execute := TRUE,
			Deceleration := rDeceleration
		);
		
		// 等待两轴都停止完成
		IF fbHaltM.Done AND fbHaltS.Done THEN
			nState := 2;
		END_IF
		
		// 错误检查
		IF fbHaltM.Error OR fbHaltS.Error THEN
			bError := TRUE;
			nState := 100;
		END_IF
		
	2: // 复位Halt功能块
		fbHaltM(Axis := AxisM, Execute := FALSE);
		fbHaltS(Axis := AxisS, Execute := FALSE);
		nState := 3;
		
	3: // 完成
		bDone := TRUE;
		bBusy := FALSE;
		nState := 0;
		
	100: // 错误状态
		bError := TRUE;
		bBusy := FALSE;
		fbHaltM(Execute := FALSE);
		fbHaltS(Execute := FALSE);
		// 等待bExecute复位
		IF NOT bExecute THEN
			nState := 0;
		END_IF
END_CASE


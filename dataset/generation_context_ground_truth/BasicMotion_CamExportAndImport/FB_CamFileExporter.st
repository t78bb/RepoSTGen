VAR
	fbWriteCam		:	SMC_WriteCAM;	// 凸轮写入功能块
	fbRtrigExecute	:	R_TRIG;			// 执行上升沿检测
	nState			:	BYTE;			// 内部状态机
END_VAR

fbRtrigExecute(CLK := bExecute);

CASE nState OF
	0: // 空闲/初始化
		bDone := FALSE;
		bBusy := FALSE;
		bError := FALSE;
		nErrorID := 0;
		fbWriteCam(bExecute := FALSE);
		
		IF fbRtrigExecute.Q THEN
			nState := 1;
			bBusy := TRUE;
		END_IF
		
	1: // 执行导出
		fbWriteCam(
			cam := camRef,
			bExecute := TRUE,
			sFileName := sFileName
		);
		
		IF fbWriteCam.bDone THEN
			fbWriteCam(bExecute := FALSE); // 复位执行信号
			nState := 2;
		ELSIF fbWriteCam.bError THEN
			bError := TRUE;
			nErrorID := fbWriteCam.nErrorID;
			fbWriteCam(bExecute := FALSE);
			nState := 100;
		END_IF
		
	2: // 完成
		bDone := TRUE;
		bBusy := FALSE;
		nState := 0;
		
	100: // 错误状态
		bError := TRUE;
		bBusy := FALSE;
		// 等待bExecute复位
		IF NOT bExecute THEN
			nState := 0;
		END_IF
END_CASE


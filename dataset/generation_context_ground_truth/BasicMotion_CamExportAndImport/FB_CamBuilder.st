VAR
	camBuilder		:	SMCB.CamBuilder;	// 凸轮构建器实例
	fbRtrigExecute	:	R_TRIG;			// 执行上升沿检测
	nState			:	BYTE;			// 内部状态机
END_VAR

fbRtrigExecute(CLK := bExecute);

CASE nState OF
	0: // 空闲/初始化
		bDone := FALSE;
		bBusy := FALSE;
		bError := FALSE;
		errorID := SMC_NO_ERROR;
		
		IF fbRtrigExecute.Q THEN
			nState := 1;
			bBusy := TRUE;
		END_IF
		
	1: // 初始化CamBuilder
		camBuilder.Init();
		nState := 2;
		
	2: // 添加凸轮段
		// 添加第一段：Poly5多项式（隐式边界）
		camBuilder.Append(SMCB.Poly5(SMCB.BoundImplicit(), SMCB.BoundImplicit())); 
		
		// 添加第二段：直线段
		camBuilder.Append(SMCB.Line(SMCB.Bound(160, 140, 2), SMCB.Bound(200, 220, 2))); 
		
		// 添加第三段：Poly5多项式（部分隐式边界）
		camBuilder.Append(SMCB.Poly5(SMCB.BoundImplicit(), SMCB.Bound(360, 360, 0, 0)));
		
		nState := 3;
		
	3: // 检查错误
		IF camBuilder.IsErrorPending(errorID => errorID) THEN
			bError := TRUE;
			nState := 100; // 跳转到错误状态
		ELSE
			nState := 4;
		END_IF
		
	4: // 初始化凸轮引用
		SMCB.InitCamRef(camRef, pSegments, nSegmentsSize);
		nState := 5;
		
	5: // 写入凸轮数据
		errorID := camBuilder.Write(camRef);
		
		IF errorID = SMC_NO_ERROR THEN
			nState := 6;
		ELSE
			bError := TRUE;
			nState := 100;
		END_IF
		
	6: // 完成
		bDone := TRUE;
		bBusy := FALSE;
		nState := 0; // 返回空闲状态
		
	100: // 错误状态
		bError := TRUE;
		bBusy := FALSE;
		// 等待bExecute复位
		IF NOT bExecute THEN
			nState := 0;
		END_IF
END_CASE


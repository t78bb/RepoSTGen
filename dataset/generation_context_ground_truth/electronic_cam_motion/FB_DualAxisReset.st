VAR
	fbReset1		:	MC_Reset;			//轴1复位
	fbReset2		:	MC_Reset;			//轴2复位
	fbReadStatus1	:	MC_ReadStatus;		//轴1状态读取
	fbReadStatus2	:	MC_ReadStatus;		//轴2状态读取
	bError1			:	BOOL;				//轴1错误标志
	bError2			:	BOOL;				//轴2错误标志
	nState			:	UDINT;				//状态机
END_VAR

CASE nState OF 
	0: (* 空闲状态 *)
		bDone := FALSE;
		bBusy := FALSE;
		
		IF bExecute THEN
			// 初始化
			fbReset1(Axis := Axis1, Execute := FALSE);
			fbReset2(Axis := Axis2, Execute := FALSE);
			fbReadStatus1(Axis := Axis1, Enable := FALSE);
			fbReadStatus2(Axis := Axis2, Enable := FALSE);
			nState := 1;
		END_IF
		
	1: (* 读取轴状态 *)
		bBusy := TRUE;
		
		fbReadStatus1(Axis := Axis1, Enable := TRUE);
		fbReadStatus2(Axis := Axis2, Enable := TRUE);
		
		IF fbReadStatus1.Valid AND fbReadStatus2.Valid THEN
			bError1 := fbReadStatus1.Errorstop;
			bError2 := fbReadStatus2.Errorstop;
			fbReadStatus1(Axis := Axis1, Enable := FALSE);
			fbReadStatus2(Axis := Axis2, Enable := FALSE);
			nState := 2;
		END_IF
		
	2: (* 执行复位 *)
		fbReset1(Axis := Axis1, Execute := TRUE);
		fbReset2(Axis := Axis2, Execute := TRUE);
		fbReadStatus1(Axis := Axis1, Enable := TRUE);
		fbReadStatus2(Axis := Axis2, Enable := TRUE);
		
		IF fbReadStatus1.Valid AND fbReadStatus2.Valid THEN
			bError1 := fbReadStatus1.Errorstop;
			bError2 := fbReadStatus2.Errorstop;
			fbReadStatus1(Axis := Axis1, Enable := FALSE);
			fbReadStatus2(Axis := Axis2, Enable := FALSE);
			
			// 检查是否还有错误
			IF NOT bError1 AND NOT bError2 THEN
				bDone := TRUE;
				bBusy := FALSE;
				nState := 3;
			ELSE
				bError := TRUE;
				bBusy := FALSE;
				nState := 3;
			END_IF
		END_IF
		
	3: (* 完成状态 *)
		IF NOT bExecute THEN
			bDone := FALSE;
			bError := FALSE;
			nState := 0;
		END_IF
END_CASE


PROGRAM PLC_PRG
VAR
	i	:	USINT;
	j	:	USINT;
	
	fbCloseRtrig	:	Standard.R_TRIG;  //电梯里Colse按钮的上升触发沿
	fbOpenRtrig		:	Standard.R_TRIG;  //电梯里Open按钮的上升触发沿
	fbHelpRtrig	:	Standard.R_TRIG;  //电梯里Alarm按钮的上升触发沿
	fbGoFloorRtrig	:	ARRAY[1..MaxNumFloor] OF Standard.R_TRIG;  //电梯里1/2/3/4按钮的上升触发沿
	fbRespondHelpRtrig	:	Standard.R_TRIG; // 电梯外面应答报警按钮的上升触发沿
	fbResetRtrig	:	Standard.R_TRIG; // 电梯外面复位按钮的上升触发沿
	fbFloorUpRtrig		:	ARRAY[1..MaxNumFloor - 1] OF Standard.R_TRIG; // 电梯外面上按钮的上升触发沿
	fbFloorDownRtrig	:	ARRAY[2..MaxNumFloor] OF Standard.R_TRIG; // 电梯外面下按钮的上升触发沿
	fbIsFloorRtrig		:	ARRAY[1..MaxNumFloor] OF Standard.R_TRIG;  // 电梯是否到位
	fbIsStopFloorRtrig	:	ARRAY[1..MaxNumFloor] OF Standard.R_TRIG;  //电梯要在哪层停止的上升触发沿
	bStopping	:	BOOL;  //处在停止状态
	bWaitClose	:	BOOL;  //等待关闭
	fbTon	:	Standard.TON;
	fbTonOpen	:	Standard.TON;
	bUpHasJob	:	BOOL;  //有要向上运动的工作
	bDownHasJob	:	BOOL; //有要向下运动的工作
	bTrigArrive	:	BOOL;// 运动到该层的到达
	bArrive	:	BOOL;//电梯本来就停在该层
	
	fbIsOpenRtrig	:	Standard.R_TRIG;  //是否处于开的状态
	fbIsCloseRtrig	:	Standard.R_TRIG;   //是否处于关的状态
END_VAR

//检测是否按下求救
fbHelpRtrig(CLK := ICallHelp);
IF fbHelpRtrig.Q THEN
	//按下求救开关，报警铃响
	QHelpBeer := TRUE;
END_IF

//检测是否应答求救
fbRespondHelpRtrig(CLK := IRespondHelp);
IF fbRespondHelpRtrig.Q THEN
	QHelpBeer := FALSE;//已经应答了求救，报警声停
END_IF

//检测是否按下复位按钮
fbResetRtrig(CLK := IReset);
IF fbResetRtrig.Q THEN
	//按下复位，忽略之前及后来的指令，电梯停到1楼
	Tar_Dir.IsBlock := TRUE;
	FOR i := 1 TO MaxNumFloor DO
		Tar_Dir.IsStopFloor[i] := FALSE;
		QGoFloorLed[i] := FALSE;
	END_FOR
	FOR i := 1 TO MaxNumFloor - 1 DO
		Tar_Dir.IsUpStop[i] := FALSE;
		QFloorUpLed[i] := FALSE;
	END_FOR
	FOR i := 2 TO MaxNumFloor DO
		Tar_Dir.IsDownStop[i] := FALSE;
		QFloorDownLed[i] := FALSE;
	END_FOR
	Tar_Dir.IsStopFloor[1] := TRUE;
	Tar_Dir.IsUpStop[1] := TRUE;
	
	Tar_Dir.IsPositive := FALSE;
	Tar_Dir.IsNegative := TRUE;
	QMotorPositiveRun := FALSE;
	QMotorNegativeRun := TRUE;
END_IF

//判断电梯目前处于第几层
FOR i := 1 TO MaxNumFloor DO
	fbIsFloorRtrig[i](CLK := IIsFloor[i]);
	IF fbIsFloorRtrig[i].Q THEN
		Tar_Dir.IsInWhichFloor := i;//保存当前电梯处于第几层
	END_IF
END_FOR

//电梯内的开关按钮操作
IF (NOT QMotorNegativeRun) AND (NOT QMotorPositiveRun) THEN
	//电梯停止在楼层，可以在电梯里手动控制电梯开关
	fbCloseRtrig(CLK := IClose);
	fbOpenRtrig(CLK := IOpen);
	IF fbCloseRtrig.Q THEN
		QClose := TRUE;//关门
		QOpen := FALSE;
	END_IF
	IF fbOpenRtrig.Q THEN
		QOpen := TRUE;//开门
		QClose := FALSE;
	END_IF
END_IF

//在电梯里选择目标的楼层，不可取消选择                                  ///哪层被按下了哪层亮
FOR i := 1 TO MaxNumFloor DO  
	fbGoFloorRtrig[i](CLK := IGoFloor[i]);
	IF fbGoFloorRtrig[i].Q AND NOT Tar_Dir.IsBlock THEN
		QGoFloorLed[i] := TRUE;
	END_IF
END_FOR

//各楼层电梯外面选择目标楼层，不可取消                            ///哪层被按下了哪层亮
FOR i := 1 TO MaxNumFloor - 1 DO //1、2、3楼的上升按钮
	fbFloorUpRtrig[i](CLK := IFloorUp[i]);
	IF fbFloorUpRtrig[i].Q AND NOT Tar_Dir.IsBlock THEN
		QFloorUpLed[i] := TRUE;
	END_IF
END_FOR
FOR i := 2 TO MaxNumFloor DO //2、3、4楼的下降按钮
	fbFloorDownRtrig[i](CLK := IFloorDown[i]);
	IF fbFloorDownRtrig[i].Q AND NOT Tar_Dir.IsBlock THEN
		QFloorDownLed[i] := TRUE;
	END_IF
END_FOR

UpdateTarget();      //更新数据结构Target_Direction中的指令状态信息

//由方向和目标楼层决定电梯的动作
IF Tar_Dir.IsPositive AND NOT bStopping THEN
	FOR i := Tar_Dir.IsInWhichFloor TO MaxNumFloor DO
		IF Tar_Dir.IsStopFloor[i] THEN   //从当前层到最高层是否有目标楼层（电梯要停止的楼层）
			QMotorPositiveRun := TRUE;//电梯上行
			EXIT;
		END_IF
	END_FOR
END_IF

IF Tar_Dir.IsNegative AND not bStopping THEN
	FOR i := 1 TO Tar_Dir.IsInWhichFloor DO
		IF Tar_Dir.IsStopFloor[i] THEN  //从最底层到当前层是否有目标楼层（电梯要停止的楼层）
			QMotorNegativeRun := TRUE;//电梯下行
			EXIT;
		END_IF
	END_FOR
END_IF

//根据电梯碰到楼层的到位开关决定电梯的动作
FOR i := 1 TO MaxNumFloor DO 
	//fbIsFloorRtrig1[i](CLK := IIsFloor[i]);
	fbIsStopFloorRtrig[i](CLK := Tar_Dir.IsStopFloor[i]);
	IF IIsFloor[i] AND fbIsStopFloorRtrig[i].Q THEN         ///电梯本来已经在目标层  电梯本来停在i层而且i层就是目标楼层（电梯要停止的楼层）
		bArrive := TRUE;
	ELSE
		bArrive := FALSE;
	END_IF
	
	IF fbIsFloorRtrig[i].Q AND Tar_Dir.IsStopFloor[i] THEN ///电梯运动到目标层   i层是目标楼层而且电梯运动到了该层
		bTrigArrive := TRUE;
	ELSE
		bTrigArrive := FALSE;
	END_IF
	
	IF bArrive OR bTrigArrive THEN           /// 若电梯停在了目标层i层，则将要在QGoFloorLed数组中将该层的值置为FALSE
		IF QGoFloorLed[i] THEN
			QGoFloorLed[i] := FALSE;
		END_IF
		CASE i OF
			1:(* 首层 *)
				IF Tar_Dir.IsUpStop[1] THEN
					QMotorNegativeRun := FALSE;//电梯停止
					bStopping := TRUE;//电梯停止，等待开门与关门
					QOpen := TRUE;//开电梯门
					QClose := FALSE;
					// 清除首层上升停靠标志
					F_ClearFloorStop(1, TRUE, FALSE, TRUE);
				END_IF
				IF Tar_Dir.IsBlock THEN
					Tar_Dir.IsBlock := FALSE;
				END_IF
				// 检查向上是否有任务
				bUpHasJob := F_CheckJobInDirection(i + 1, MaxNumFloor, TRUE);
				bDownHasJob := FALSE;
			MaxNumFloor:(* 顶层 *)
				IF Tar_Dir.IsDownStop[MaxNumFloor] THEN
					QMotorPositiveRun := FALSE;//电梯停止
					bStopping := TRUE;//电梯停止，等待开门与关门
					QOpen := TRUE;//开电梯门
					QClose := FALSE;
					// 清除顶层下降停靠标志
					F_ClearFloorStop(MaxNumFloor, FALSE, TRUE, TRUE);
				END_IF
				// 检查向下是否有任务
				bDownHasJob := F_CheckJobInDirection(1, i - 1, TRUE);
				bUpHasJob := FALSE;
			ELSE(* 中间层 *)
				IF Tar_Dir.IsPositive THEN
					// 检查向上是否有任务
					bUpHasJob := F_CheckJobInDirection(i + 1, MaxNumFloor, TRUE);
				END_IF
				IF (Tar_Dir.IsPositive AND Tar_Dir.IsUpStop[i]) OR (Tar_Dir.IsPositive AND (NOT bUpHasJob) AND Tar_Dir.IsDownStop[i])THEN
					QMotorPositiveRun := FALSE;//电梯停止
					bStopping := TRUE;//电梯停止，等待开门与关门
					QOpen := TRUE;//开电梯门
					QClose := FALSE;
					IF Tar_Dir.IsUpStop[i] THEN
						// 清除上升停靠标志
						F_ClearFloorStop(i, TRUE, FALSE, NOT Tar_Dir.IsDownStop[i]);
					END_IF
					IF (NOT bUpHasJob) AND Tar_Dir.IsDownStop[i] THEN
						// 清除下降停靠标志
						F_ClearFloorStop(i, FALSE, TRUE, TRUE);
					END_IF
				END_IF
				
				IF Tar_Dir.IsNegative THEN
					// 检查向下是否有任务
					bDownHasJob := F_CheckJobInDirection(1, i - 1, TRUE);
				END_IF
				IF (Tar_Dir.IsNegative AND Tar_Dir.IsDownStop[i]) OR (Tar_Dir.IsNegative AND (NOT bDownHasJob) AND Tar_Dir.IsUpStop[i])THEN
					QMotorNegativeRun := FALSE;//电梯停止
					bStopping := TRUE;//电梯停止，等待开门与关门
					QOpen := TRUE;//开电梯门
					QClose := FALSE;
					IF Tar_Dir.IsDownStop[i] THEN
						// 清除下降停靠标志
						F_ClearFloorStop(i, FALSE, TRUE, NOT Tar_Dir.IsUpStop[i]);
					END_IF
					IF (NOT bDownHasJob) AND Tar_Dir.IsUpStop[i] THEN
						// 清除上升停靠标志
						F_ClearFloorStop(i, TRUE, FALSE, TRUE);
					END_IF
				END_IF
				
				IF (NOT Tar_Dir.IsNegative AND NOT Tar_Dir.IsPositive) THEN
					bStopping := TRUE;//电梯停止，等待开门与关门
					QOpen := TRUE;//开电梯门
					QClose := FALSE;
					// 清除所有停靠标志
					F_ClearFloorStop(i, TRUE, TRUE, TRUE);
				END_IF
		END_CASE
	
		IF Tar_Dir.IsPositive AND bUpHasJob THEN  //当电梯处在上行状态且有向上运动的工作，则电梯状态为上升
			Tar_Dir.IsPositive := TRUE;
			Tar_Dir.IsNegative := FALSE;
		END_IF
		IF Tar_Dir.IsPositive AND (NOT bUpHasJob) AND bDownHasJob THEN  //当电梯处在上行状态、没有向上运动的工作，但有下行的工作，则电梯状态置为下降
			Tar_Dir.IsPositive := FALSE;
			Tar_Dir.IsNegative := TRUE;
		END_IF
		IF Tar_Dir.IsNegative AND bDownHasJob THEN  //当电梯处在下行状态且有向下运动的工作，则电梯状态为下降
			Tar_Dir.IsPositive := FALSE;
			Tar_Dir.IsNegative := TRUE;
		END_IF
		IF Tar_Dir.IsNegative AND (NOT bDownHasJob) AND bUpHasJob THEN //当电梯处在下行状态、没有向下运动的工作，但有上行的工作，则电梯状态置为上升
			Tar_Dir.IsPositive := TRUE;
			Tar_Dir.IsNegative := FALSE;
		END_IF
		
		IF bUpHasJob OR bDownHasJob THEN
			Tar_Dir.IsFree := FALSE;
		ELSE
			Tar_Dir.IsFree := TRUE;
			Tar_Dir.IsPositive := FALSE;
			Tar_Dir.IsNegative := FALSE;
		END_IF
	END_IF
END_FOR

//门开了5秒后，关门
fbIsOpenRtrig(CLK := IIsOpen);
IF fbIsOpenRtrig.Q THEN
	bWaitClose := TRUE;
END_IF

fbTonOpen(IN := bWaitClose,PT := T#5S);
IF fbTonOpen.Q THEN
	bWaitClose := FALSE;
	QClose := TRUE;
	QOpen := FALSE;
END_IF

//电梯门关到位后，停止状态清零，电梯可运动
fbIsCloseRtrig(CLK := IIsClose);
IF fbIsCloseRtrig.Q THEN
	bStopping := FALSE;
END_IF

HMI(); // 设定电梯上升下降时间等以及视图中箭头的隐藏与显示


PROGRAM UpdateTarget
VAR
	i	:	USINT;
	//j	:	USINT;
	fbGoFloorLedRtrig	:	ARRAY[1..MaxNumFloor] OF Standard.R_TRIG;   //视图中“1/2/3/4”按钮触发的上升沿
	fbFloorUpLedRtrig	:	ARRAY[1..MaxNumFloor - 1] OF Standard.R_TRIG;  //视图中3个“上”按钮触发的上升沿
	fbFloorDownLedRtrig	:	ARRAY[2..MaxNumFloor] OF Standard.R_TRIG;   //视图中3个“下”按钮触发的上升沿

END_VAR

//由电梯内外决定电梯将要进行的动作
FOR i := 1 TO MaxNumFloor - 1 DO //第1、2、3楼楼层中（电梯外面）向上的按钮
	fbFloorUpLedRtrig[i](CLK := QFloorUpLed[i]);
	IF fbFloorUpLedRtrig[i].Q THEN//判断是否有“上”按钮按下
		Tar_Dir.IsStopFloor[i] := TRUE;//之前没有记录，更新
		Tar_Dir.IsUpStop[i] := TRUE;//将上升电梯要停的楼层数组中将该层置为TRUE
		IF (Tar_Dir.IsFree = TRUE) THEN
			// 设置电梯运行方向
			F_SetElevatorDirection(Tar_Dir.IsInWhichFloor, i);
			Tar_Dir.IsFree := FALSE;
		END_IF
	END_IF
END_FOR

FOR i := 2 TO MaxNumFloor DO//第2、3、4楼楼层中（电梯外面）向下的按钮
	fbFloorDownLedRtrig[i](CLK := QFloorDownLed[i]);
	IF fbFloorDownLedRtrig[i].Q THEN
		Tar_Dir.IsStopFloor[i] := TRUE;
		Tar_Dir.IsDownStop[i] := TRUE;
		IF (Tar_Dir.IsFree = TRUE) THEN
			// 设置电梯运行方向
			F_SetElevatorDirection(Tar_Dir.IsInWhichFloor, i);
			Tar_Dir.IsFree := FALSE;
		END_IF
	END_IF
END_FOR

FOR i := 1 TO MaxNumFloor DO//电梯内的“1、2、3、4”的按钮
	fbGoFloorLedRtrig[i](CLK := QGoFloorLed[i]);
	IF fbGoFloorLedRtrig[i].Q THEN
		IF (Tar_Dir.IsStopFloor[i] <> TRUE) THEN
			Tar_Dir.IsStopFloor[i] := TRUE;
		END_IF
		IF i >= Tar_Dir.IsInWhichFloor THEN
			IF i < MaxNumFloor THEN
				Tar_Dir.IsUpStop[i] := TRUE;
			ELSE
				Tar_Dir.IsDownStop[i] := TRUE;
			END_IF
			IF Tar_Dir.IsFree THEN
				// 设置电梯运行方向（向上）
				F_SetElevatorDirection(Tar_Dir.IsInWhichFloor, i);
				Tar_Dir.IsFree := FALSE;
			END_IF
		ELSE
			IF i > 1 THEN
				Tar_Dir.IsDownStop[i] := TRUE;
			ELSE
				Tar_Dir.IsUpStop[i] := TRUE;
			END_IF
			IF Tar_Dir.IsFree THEN
				// 设置电梯运行方向（向下）
				F_SetElevatorDirection(Tar_Dir.IsInWhichFloor, i);
				Tar_Dir.IsFree := FALSE;
			END_IF
		END_IF
	END_IF
END_FOR
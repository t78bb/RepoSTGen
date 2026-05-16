VAR
	i	:	USINT;
END_VAR

// 检查从起始楼层到结束楼层之间是否有电梯需要停靠的楼层
F_CheckJobInDirection := FALSE;

IF bIncreasing THEN
	// 向上检查（从低楼层到高楼层）
	FOR i := nStartFloor TO nEndFloor DO
		IF Tar_Dir.IsStopFloor[i] THEN
			F_CheckJobInDirection := TRUE;
			RETURN;
		END_IF
	END_FOR
ELSE
	// 向下检查（从高楼层到低楼层）
	FOR i := nEndFloor TO nStartFloor BY -1 DO
		IF Tar_Dir.IsStopFloor[i] THEN
			F_CheckJobInDirection := TRUE;
			RETURN;
		END_IF
	END_FOR
END_IF


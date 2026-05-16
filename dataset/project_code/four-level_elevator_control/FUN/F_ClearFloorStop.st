FUNCTION F_ClearFloorStop : BOOL
VAR_INPUT
	nFloor			:	USINT;		//楼层号
	bClearUpStop	:	BOOL;		//是否清除上升停靠标志
	bClearDownStop	:	BOOL;		//是否清除下降停靠标志
	bClearStopFloor	:	BOOL;		//是否清除楼层停靠标志
END_VAR

// 清除楼层停靠标志
IF bClearUpStop AND (nFloor <= MaxNumFloor - 1) THEN
	Tar_Dir.IsUpStop[nFloor] := FALSE;
	QFloorUpLed[nFloor] := FALSE;
END_IF

IF bClearDownStop AND (nFloor >= 2) THEN
	Tar_Dir.IsDownStop[nFloor] := FALSE;
	QFloorDownLed[nFloor] := FALSE;
END_IF

IF bClearStopFloor THEN
	Tar_Dir.IsStopFloor[nFloor] := FALSE;
END_IF

// 清除电梯内按钮LED
IF bClearStopFloor THEN
	QGoFloorLed[nFloor] := FALSE;
END_IF
F_ClearFloorStop := TRUE;

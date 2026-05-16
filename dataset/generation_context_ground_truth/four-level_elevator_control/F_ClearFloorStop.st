
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


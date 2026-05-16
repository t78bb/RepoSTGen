
// 根据当前楼层和目标楼层设定电梯运行方向
IF nTargetFloor > nCurrentFloor THEN
	// 目标楼层高于当前楼层，电梯上升
	Tar_Dir.IsPositive := TRUE;
	Tar_Dir.IsNegative := FALSE;
ELSIF nTargetFloor < nCurrentFloor THEN
	// 目标楼层低于当前楼层，电梯下降
	Tar_Dir.IsPositive := FALSE;
	Tar_Dir.IsNegative := TRUE;
END_IF
// 如果目标楼层等于当前楼层，不改变方向


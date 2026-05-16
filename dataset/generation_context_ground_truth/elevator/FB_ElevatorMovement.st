VAR
	fbMoveDelayTimer	:	TON;				// 移动延时定时器
	i					:	INT;				// 循环变量
	bHasUpperRequest	:	BOOL;				// 有更高楼层请求
	bHasLowerRequest	:	BOOL;				// 有更低楼层请求
END_VAR

// 检查是否到达目标楼层
IF TargetFloors[CurrentFloor] THEN
	bArrivedAtTarget := TRUE;
	TargetFloors[CurrentFloor] := FALSE; // 清除请求
	bMovingUp := FALSE;
	bMovingDown := FALSE;
	RETURN;
ELSE
	bArrivedAtTarget := FALSE;
END_IF

// 只有门准备好才能移动
IF NOT bDoorReady THEN
	RETURN;
END_IF

// 检查是否有更高楼层的请求
bHasUpperRequest := FALSE;
FOR i := CurrentFloor + 1 TO 3 DO
	IF TargetFloors[i] THEN
		bHasUpperRequest := TRUE;
		EXIT;
	END_IF
END_FOR

// 检查是否有更低楼层的请求
bHasLowerRequest := FALSE;
FOR i := CurrentFloor - 1 TO 0 BY -1 DO
	IF TargetFloors[i] THEN
		bHasLowerRequest := TRUE;
		EXIT;
	END_IF
END_FOR

// 移动逻辑
IF bMovingUp OR (NOT bMovingDown AND bHasUpperRequest) THEN
	// 向上移动
	IF bHasUpperRequest THEN
		fbMoveDelayTimer(IN := TRUE, PT := T#500MS);
		IF fbMoveDelayTimer.Q THEN
			bMovingUp := TRUE;
			bMovingDown := FALSE;
			fbMoveDelayTimer(IN := FALSE);
		END_IF
	ELSE
		// 没有更高请求，改变方向
		bMovingUp := FALSE;
		IF bHasLowerRequest THEN
			bMovingDown := TRUE;
		END_IF
	END_IF
ELSIF bMovingDown OR (NOT bMovingUp AND bHasLowerRequest) THEN
	// 向下移动
	IF bHasLowerRequest THEN
		fbMoveDelayTimer(IN := TRUE, PT := T#500MS);
		IF fbMoveDelayTimer.Q THEN
			bMovingDown := TRUE;
			bMovingUp := FALSE;
			fbMoveDelayTimer(IN := FALSE);
		END_IF
	ELSE
		// 没有更低请求，改变方向
		bMovingDown := FALSE;
		IF bHasUpperRequest THEN
			bMovingUp := TRUE;
		END_IF
	END_IF
ELSE
	// 初始状态，默认向上
	IF bHasUpperRequest THEN
		bMovingUp := TRUE;
	ELSIF bHasLowerRequest THEN
		bMovingDown := TRUE;
	END_IF
END_IF


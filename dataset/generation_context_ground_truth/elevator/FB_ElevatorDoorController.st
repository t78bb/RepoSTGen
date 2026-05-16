VAR
	fbDoorTimer			:	TON;		// 开门延时定时器
	fbCloseDoorTimer	:	TON;		// 关门延时定时器
	nState				:	INT;		// 状态机
END_VAR

CASE nState OF
	0: // 空闲状态
		bOpenDoor := FALSE;
		bCloseDoor := FALSE;
		bDoorReady := TRUE;
		
		IF bArrivedAtTarget THEN
			nState := 1; // 开始开门流程
		END_IF
		
	1: // 开门延时
		bCloseDoor := FALSE;
		bDoorReady := FALSE;
		fbDoorTimer(IN := TRUE, PT := T#2S);
		
		IF fbDoorTimer.Q THEN
			fbDoorTimer(IN := FALSE);
			nState := 2;
		END_IF
		
	2: // 开门
		bOpenDoor := TRUE;
		bDoorOpen := TRUE;
		nState := 3;
		
	3: // 等待开始关门
		IF NOT bArrivedAtTarget THEN
			nState := 4; // 开始关门流程
		END_IF
		
	4: // 关门
		bOpenDoor := FALSE;
		bCloseDoor := TRUE;
		bDoorOpen := FALSE;
		fbCloseDoorTimer(IN := TRUE, PT := T#2S);
		
		IF fbCloseDoorTimer.Q AND bDoorClosed THEN
			fbCloseDoorTimer(IN := FALSE);
			nState := 0; // 返回空闲
		END_IF
END_CASE


FUNCTION F_UpdateDoorAnimation : DINT
VAR_INPUT
	bOpenDoor		:	BOOL;		// 开门命令
	bCloseDoor		:	BOOL;		// 关门命令
	bCallFloor		:	BOOL;		// 该楼层有呼叫
	nCurrentAni		:	DINT;		// 当前动画值
	nMaxAni			:	DINT := 70;	// 最大动画值
END_VAR
VAR
	nNewAni			:	DINT;		// 新的动画值
END_VAR

nNewAni := nCurrentAni;

// 开门动画（增加动画值）
IF bOpenDoor AND nNewAni < nMaxAni AND bCallFloor THEN
	nNewAni := nNewAni + 1;
END_IF

// 关门动画（减少动画值）
IF bCloseDoor AND nNewAni > 0 THEN
	nNewAni := nNewAni - 1;
END_IF

F_UpdateDoorAnimation := nNewAni;


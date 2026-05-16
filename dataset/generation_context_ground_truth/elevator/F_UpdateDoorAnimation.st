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


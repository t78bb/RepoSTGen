FUNCTION_BLOCK FB_CountdownTimer
VAR_INPUT
	tElapsedTime	:	TIME;		//已经过的时间（定时器的ET）
	tTotalTime		:	TIME;		//总时间（定时器的PT）
END_VAR
VAR_OUTPUT
	nRemainingSeconds	:	UINT;	//剩余秒数
END_VAR
VAR
	nTotalSeconds		:	UINT;	//总秒数
	nElapsedSeconds		:	UINT;	//已过秒数
END_VAR

// 将TIME转换为秒
nTotalSeconds := INT_TO_USINT(TRUNC_INT(TIME_TO_DWORD(tTotalTime) / 1000.0));
nElapsedSeconds := INT_TO_USINT(TRUNC_INT(TIME_TO_UINT(tElapsedTime) / 1000.0));

// 计算剩余秒数
nRemainingSeconds := nTotalSeconds - nElapsedSeconds;


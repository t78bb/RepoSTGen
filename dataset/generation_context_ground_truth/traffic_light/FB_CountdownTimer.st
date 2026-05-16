VAR
	nTotalSeconds		:	UINT;	//总秒数
	nElapsedSeconds		:	UINT;	//已过秒数
END_VAR

// 将TIME转换为秒
nTotalSeconds := INT_TO_USINT(TRUNC_INT(TIME_TO_DWORD(tTotalTime) / 1000.0));
nElapsedSeconds := INT_TO_USINT(TRUNC_INT(TIME_TO_UINT(tElapsedTime) / 1000.0));

// 计算剩余秒数
nRemainingSeconds := nTotalSeconds - nElapsedSeconds;


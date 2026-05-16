FUNCTION F_TimeToSeconds : DWORD
VAR_INPUT
	tTime	:	TIME;		//输入的时间
END_VAR

// 将TIME类型转换为秒数（DWORD）
// TIME内部是毫秒，除以1000得到秒数
F_TimeToSeconds := DINT_TO_DWORD(TRUNC(TIME_TO_DWORD(tTime) / 1000.0));


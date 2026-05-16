FUNCTION F_SecondsToTime : TIME
VAR_INPUT
	dwSeconds	:	DWORD;		//输入的秒数
END_VAR

// 将秒数（DWORD）转换为TIME类型
// 秒数乘以1000得到毫秒
F_SecondsToTime := DWORD_TO_TIME(dwSeconds * 1000);


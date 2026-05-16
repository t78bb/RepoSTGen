FUNCTION_BLOCK FB_Counter
VAR_INPUT
	bUp:BOOL;			(*递增信号输入*)
	bDown:BOOL;			(*递减信号输入*)
	bReset:BOOL;		(*复位、清零信号输入*)
END_VAR
VAR_OUTPUT
	nValue:INT;			(*输出数值*)
END_VAR

IF bUp THEN						
	nValue:=nValue+1;	(*数据递增*)
END_IF
IF bDown THEN
	nValue:=nValue-1;	(*数据递减*)
END_IF
IF bReset THEN
	nValue:=0;			(*数据清零*)
END_IF

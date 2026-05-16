PROGRAM PLC_PRG
VAR
	FB_Counter_0:FB_Counter;
	bUp,bDown,bReset:BOOL;
	ActuallyValue:int;
END_VAR


FB_Counter_0(
    bUp := bUp,
    bDown := bDown,
    bReset := bReset
);

ActuallyValue := FB_Counter_0.nValue;

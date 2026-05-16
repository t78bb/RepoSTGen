METHOD PUBLIC SetCommand : BOOL
VAR_INPUT
	nPosition		: INT;
	iCommand		: I_Command;
    arrSwitch		: ARRAY[1..8] OF BOOL;

END_VAR
VAR
	aiCommand		: ARRAY[1..8] OF I_Command;	
	arrRtrig		: ARRAY[1..8] OF R_TRIG;
	nIndex			: INT;
END_VAR



IF ((nPosition >= 1) AND (nPosition <= 8) AND (iCommand <> 0)) THEN
	THIS^.aiCommand[nPosition] := iCommand;
END_IF

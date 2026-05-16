METHOD FB_init : BOOL
VAR_INPUT
	bInitRetains : BOOL; // if TRUE, the retain variables are initialized (warm start / cold start)
	bInCopyCode : BOOL;  // if TRUE, the instance afterwards gets moved into the copy code (online change)
    arrSwitch		: ARRAY[1..8] OF BOOL;
END_VAR
VAR
	nIndex : INT;
    aiCommand		: ARRAY[1..8] OF I_Command;	
	arrRtrig		: ARRAY[1..8] OF R_TRIG;
	nIndex			: INT;
END_VAR



FOR nIndex := 1 TO 8 DO
	aiCommand[nIndex] := 0;
END_FOR



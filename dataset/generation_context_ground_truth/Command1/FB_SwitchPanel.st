VAR
	aiCommand		: ARRAY[1..8] OF I_Command;	
	arrRtrig		: ARRAY[1..8] OF R_TRIG;
	nIndex			: INT;
END_VAR

FOR nIndex := 1 TO 8 DO
	arrRtrig[nIndex](CLK := arrSwitch[nIndex]);
	IF arrRtrig[nIndex].Q THEN
		IF (aiCommand[nIndex] <> 0) THEN
			aiCommand[nIndex].Execute();
		END_IF
	END_IF
END_FOR

METHOD mLiga : BOOL
VAR_INPUT
	entrada:BOOL;
END_VAR
VAR_OUTPUT
	saida:BOOL;
END_VAR
VAR
	Timer:ton;
	tempo:TIME;
END_VAR

Timer(IN:=TRUE , PT:=tempo);

IF Timer.Q THEN
	saida:=TRUE;
    Timer(IN:=FALSE);
END_IF
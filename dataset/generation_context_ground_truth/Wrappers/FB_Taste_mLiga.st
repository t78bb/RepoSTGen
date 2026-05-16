VAR
	Timer:ton;
	tempo:TIME;
END_VAR

Timer(IN:=TRUE , PT:=tempo);

IF Timer.Q THEN
	saida:=TRUE;
    Timer(IN:=FALSE);
END_IF
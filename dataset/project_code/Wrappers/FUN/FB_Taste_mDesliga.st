METHOD mDesliga : BOOL
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

saida:=FALSE;
Timer(IN:=false);
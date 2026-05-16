METHOD SetTempo : BOOL
VAR_INPUT
	delay:TIME;
	entrada:BOOL;
END_VAR
VAR_OUTPUT
	saida:BOOL;
END_VAR
VAR
	Timer:ton;
	tempo:TIME;
END_VAR

tempo:=delay;
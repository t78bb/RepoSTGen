METHOD Map : BOOL
VAR
	index:int;
    fb_teste:array [1..3] of FB_Teste;
	index: INT;
END_VAR
VAR_INPUT
	in:BOOL;
END_VAR
VAR_OUTPUT
	out:BOOL;
END_VAR

FOR index:= 1 TO 3 DO

fb_teste[index].entrada:=in;
out:=fb_teste[index].saida;

END_FOR
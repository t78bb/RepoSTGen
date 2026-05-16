FUNCTION_BLOCK FB_Wrapper
VAR_INPUT
	in:BOOL;
END_VAR
VAR_OUTPUT
	out:BOOL;
END_VAR
VAR
	fb_teste:array [1..3] of FB_Teste;
	index: INT;
END_VAR

Map();


fb_teste[1].SetTempo(delay:=T#4S);
fb_teste[2].SetTempo(delay:=T#1S);
fb_teste[3].SetTempo(delay:=T#2S);

FOR index := 1 TO 3 DO
IF in THEN
	fb_teste[index].mLiga();
ELSE
	fb_teste[index].mDesliga();
END_IF

END_FOR
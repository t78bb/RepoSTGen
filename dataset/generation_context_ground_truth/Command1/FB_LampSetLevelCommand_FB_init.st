VAR
	refLamp		: REFERENCE TO FB_Lamp;
	byNewLevel	: BYTE;
END_VAR

IF (__ISVALIDREF(refLamp)) THEN
	THIS^.refLamp REF= refLamp;
ELSE
	THIS^.refLamp REF= 0;
END_IF
THIS^.byNewLevel := byNewLevel;
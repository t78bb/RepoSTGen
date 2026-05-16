METHOD FB_init : BOOL
VAR_INPUT
	bInitRetains : BOOL; // if TRUE, the retain variables are initialized (warm start / cold start)
	bInCopyCode : BOOL;  // if TRUE, the instance afterwards gets moved into the copy code (online change)
	refLamp : REFERENCE TO FB_Lamp;
	byNewLevel : BYTE;
END_VAR
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
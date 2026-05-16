VAR
	refCDPlayer : REFERENCE TO FB_CDPlayer;
END_VAR

IF (__ISVALIDREF(refCDPlayer)) THEN
	THIS^.refCDPlayer REF= refCDPlayer;
ELSE
	THIS^.refCDPlayer REF= 0;
END_IF
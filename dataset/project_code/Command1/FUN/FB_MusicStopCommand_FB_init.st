METHOD FB_init : BOOL
VAR_INPUT
	bInitRetains : BOOL; // if TRUE, the retain variables are initialized (warm start / cold start)
	bInCopyCode : BOOL;  // if TRUE, the instance afterwards gets moved into the copy code (online change)
	refCDPlayer : REFERENCE TO FB_CDPlayer;
END_VAR
VAR
	refCDPlayer : REFERENCE TO FB_CDPlayer;
END_VAR

IF (__ISVALIDREF(refCDPlayer)) THEN
	THIS^.refCDPlayer REF= refCDPlayer;
ELSE
	THIS^.refCDPlayer REF= 0;
END_IF
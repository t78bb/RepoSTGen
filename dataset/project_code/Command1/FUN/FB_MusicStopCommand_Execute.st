METHOD Execute
VAR
	refCDPlayer : REFERENCE TO FB_CDPlayer;
END_VAR

IF (__ISVALIDREF(THIS^.refCDPlayer)) THEN
	THIS^.refCDPlayer.Stop();
END_IF

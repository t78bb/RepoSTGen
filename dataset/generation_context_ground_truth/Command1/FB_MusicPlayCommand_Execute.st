VAR
	refCDPlayer : REFERENCE TO FB_CDPlayer;
END_VAR

IF (__ISVALIDREF(THIS^.refCDPlayer)) THEN
	THIS^.refCDPlayer.SetVolume(40);
	THIS^.refCDPlayer.SetTrack(1);
	THIS^.refCDPlayer.Start();
END_IF

PROGRAM TrafficLigthHMI
VAR
	greenTimeOn		:	DWORD := F_TimeToSeconds(MGreenTimeOn);		//绿灯亮的时间（秒）
	greenTimeFlash	:	DWORD := F_TimeToSeconds(MGreenTimeFlash);	//绿灯闪的时间（秒）
	yellowTimeOn	:	DWORD := F_TimeToSeconds(MYellowTimeOn);	//黄灯亮的时间（秒）
	bSave	:	BOOL;
	fbSaveRtrig	:	R_TRIG;
END_VAR

fbSaveRtrig(CLK := bSave);
IF fbSaveRtrig.Q THEN
	MGreenTimeOn := F_SecondsToTime(greenTimeOn);
	MGreenTimeFlash := F_SecondsToTime(greenTimeFlash);
	MYellowTimeOn := F_SecondsToTime(yellowTimeOn);
END_IF
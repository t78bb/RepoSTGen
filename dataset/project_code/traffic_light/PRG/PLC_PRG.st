PROGRAM PLC_PRG
VAR
	fbTon	:	TON;
	fbTon1	:	TON;
	nState	:	USINT;
	fbResetRtrig	:	R_TRIG;
	temp	:	UINT;
	fbCountdown	:	FB_CountdownTimer;	//倒计时计算功能块
END_VAR

fbResetRtrig(CLK := IReset);
IF fbResetRtrig.Q THEN
	fbTon(IN := FALSE);
	fbTon1(IN := FALSE);
	QSouthNorthGreen := FALSE;
	QSouthNorthYellow := FALSE;
	QSouthNorthRed := FALSE;
	QEastWestGreen := FALSE;
	QEastWestYellow := FALSE;
	QEastWestRed := FALSE;
	MCountBackwards := 0;
	nState := 0;
END_IF

CASE nState OF 
	0:
		QSouthNorthGreen := TRUE;//南北绿灯亮
		QEastWestGreen := FALSE;//东西方向绿灯灭
		QEastWestRed := TRUE;//东西方向红灯亮
		QEastWestYellow := FALSE;//东西方向黄灯灭
		QSouthNorthRed := FALSE;//南北方向红灯灭
		fbTon(IN := TRUE,PT := MGreenTimeOn);//定时，定时到后，绿灯开始闪
		IF fbTon.Q THEN
			fbTon(IN := FALSE);
			QSouthNorthGreen := FALSE;//南北绿灯灭，准备开始闪
		//	QEastWestRed := FALSE;
			nState := 1;
		END_IF
		//计算倒计时
		fbCountdown(tElapsedTime := fbTon.ET, tTotalTime := MGreenTimeOn);
		temp := fbCountdown.nRemainingSeconds;
	1:
		fbTon(IN := TRUE,PT := MGreenTimeFlash);//定时，定时到后，绿灯灭，黄灯亮
		fbTon1(IN := TRUE,PT := T#0.3S);//定时0.5s，绿灯闪烁
		IF fbTon1.Q THEN
			QSouthNorthGreen := NOT QSouthNorthGreen;
			fbTon1(IN := FALSE);//定时0.5s，绿灯闪烁
		END_IF
		IF fbTon.Q THEN
			fbTon(IN := FALSE);
			QSouthNorthGreen := FALSE;//南北绿灯灭
			nState := 2;
		END_IF
		//计算倒计时
		fbCountdown(tElapsedTime := fbTon.ET, tTotalTime := MGreenTimeFlash);
		temp := fbCountdown.nRemainingSeconds;
	2:
		QSouthNorthYellow := TRUE;//南北黄灯亮
		fbTon(IN := TRUE,PT := MYellowTimeOn);//定时，定时到后，黄灯灭
		IF fbTon.Q THEN
			fbTon(IN := FALSE);
			QSouthNorthYellow := FALSE;//南北黄灯灭
			nState := 3;
		END_IF
		//计算倒计时
		fbCountdown(tElapsedTime := fbTon.ET, tTotalTime := MYellowTimeOn);
		temp := fbCountdown.nRemainingSeconds;
	3:
		QSouthNorthGreen := FALSE;//南北绿灯灭
		QSouthNorthRed := TRUE;//南北方向红灯亮
		QSouthNorthYellow := FALSE;//南北方向黄灯灭
		QEastWestGreen := TRUE;////东西方向绿灯亮
		QEastWestRed := FALSE;//东西方向红灯灭
		fbTon(IN := TRUE,PT := MGreenTimeOn);//定时，定时到后，绿灯开始闪
		IF fbTon.Q THEN
			fbTon(IN := FALSE);
			QEastWestGreen := FALSE;//东西方向绿灯开始闪
			nState := 4;
		END_IF
		//计算倒计时
		fbCountdown(tElapsedTime := fbTon.ET, tTotalTime := MGreenTimeOn);
		temp := fbCountdown.nRemainingSeconds;
	4:
		fbTon(IN := TRUE,PT := MGreenTimeFlash);//定时，定时到后，绿灯灭，黄灯亮
		fbTon1(IN := TRUE,PT := T#0.3S);//定时0.5s，绿灯闪烁
		IF fbTon1.Q THEN
			QEastWestGreen := NOT QEastWestGreen;
			fbTon1(IN := FALSE);//定时0.5s，绿灯闪烁
		END_IF
		IF fbTon.Q THEN
			fbTon(IN := FALSE);
			QEastWestGreen := FALSE;//东西方向绿灯灭
			nState := 5;
		END_IF
		//计算倒计时
		fbCountdown(tElapsedTime := fbTon.ET, tTotalTime := MGreenTimeFlash);
		temp := fbCountdown.nRemainingSeconds;
	5:
		QEastWestYellow := TRUE;//东西方向黄灯亮
		fbTon(IN := TRUE,PT := MYellowTimeOn);//定时，定时到后，黄灯灭
		IF fbTon.Q THEN
			fbTon(IN := FALSE);
			QEastWestYellow := FALSE;//东西方向黄灯灭
			nState := 0;
		END_IF
		//计算倒计时
		fbCountdown(tElapsedTime := fbTon.ET, tTotalTime := MYellowTimeOn);
		temp := fbCountdown.nRemainingSeconds;
END_CASE

MCountBackwards := temp;
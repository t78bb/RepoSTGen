
IF pidMode THEN 	//pid模式，没有动作指令时不执行输出
	
	IF NOT manualPidPrmSet THEN
		FOR gi := 1 TO 10 DO
			 IF gDev.grd[gi].vector = TargetDirect.stop THEN
				cmdExecutor(level := 1, idx := gi, percent := 0);
			 END_IF
		END_FOR
		
		FOR si := 1 TO 10 DO
			IF gDev.sky[si].vector = TargetDirect.stop THEN		
				cmdExecutor(level := 2, idx := si, percent := 0);
			END_IF
		END_FOR
		//起竖挡板执行开关量特判
		IF gDev.sky[0].vector = TargetDirect.stop THEN 
			cmdExecutor(level := 2, idx := 0, percent := 0);
		END_IF
	END_IF
ELSE		//开关量控制
	
	FOR gi := 1 TO 10 DO
		 IF gDev.grd[gi].vector = TargetDirect.stop THEN
			gUI.grd[gi].pwrEnable := FALSE;
		 ELSE
			gUI.grd[gi].pwrEnable := TRUE;
		 END_IF
	END_FOR
	
	FOR si := 0 TO 10 DO
		IF gDev.sky[si].vector = TargetDirect.stop THEN		
			gUI.sky[si].pwrEnable := FALSE;
		ELSE													
			gUI.sky[si].pwrEnable := TRUE;	
		END_IF
	END_FOR
END_IF

(*
FOR gi := 1 TO 10 DO
	 IF gDev.grd[gi].vector <> TargetDirect.stop THEN
		IF pidMode THEN
			cmdExecutor(level := 1, idx := gi, percent := grdPid[gi].res);
		ELSE
			gUI.grd[gi].pwrEnable := TRUE;
		END_IF
	 ELSE
		IF pidMode THEN
			cmdExecutor(level := 1, idx := gi, percent := 0);
		ELSE
			gUI.grd[gi].pwrEnable := FALSE;
		END_IF
	 END_IF
END_FOR


FOR si := 1 TO 10 DO
	IF gDev.sky[si].vector <> TargetDirect.stop THEN		//运动状态，执行  PID或开关使能
		IF pidMode THEN
			cmdExecutor(level := 2, idx := si, percent := skyPid[si].res);
		ELSE
			gUI.sky[si].pwrEnable := TRUE;	
		END_IF
	ELSE													//停止状态，关闭 PID或开关使能
		IF pidMode THEN
			cmdExecutor(level := 2, idx := si, percent := 0);
		ELSE
			gUI.sky[si].pwrEnable := FALSE;
		END_IF
	END_IF
END_FOR

IF gDev.sky[0].vector <> TargetDirect.stop THEN
	gUI.sky[0].pwrEnable := TRUE;
	IF gDev.sky[0].vector = TargetDirect.extend THEN	cmdExecutor(level := 2, idx := 0, percent := gDev.sky[0].ctrl.exPct);END_IF
	IF gDev.sky[0].vector = TargetDirect.retract THEN	cmdExecutor(level := 2, idx := 0, percent := -gDev.sky[0].ctrl.rtPct);END_IF
ELSE
	gUI.sky[0].pwrEnable := FALSE;
	cmdExecutor(level := 2, idx := 0, percent := 0);
END_IF
*)

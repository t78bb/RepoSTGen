METHOD pidExecute
VAR_INPUT
END_VAR
VAR
	vector 		:TargetDirect;
END_VAR

FOR gi := 1 TO 10 DO
	IF gDev.grd[gi].ctrl.isError THEN
		CONTINUE;
	END_IF
	cmdExecutor(level := 1, idx := gi, percent := grdPid[gi].res);
END_FOR


FOR si := 1 TO 10 DO
	IF gDev.sky[si].ctrl.isError THEN
		CONTINUE;
	END_IF
	cmdExecutor(level := 2, idx := si, percent := skyPid[si].res);
END_FOR

//起竖挡板执行开关量
IF NOT gDev.sky[0].ctrl.isError THEN
	IF gDev.sky[0].vector = TargetDirect.extend THEN
		cmdExecutor(level := 2, idx := 0, percent := gDev.sky[0].ctrl.exPct);
	END_IF
	IF gDev.sky[0].vector = TargetDirect.retract THEN
		cmdExecutor(level := 2, idx := 0, percent := -gDev.sky[0].ctrl.rtPct);
	END_IF
END_IF
(*
IF NOT gDev.grd[7].ctrl.isError THEN
	IF gDev.grd[7].vector = TargetDirect.extend THEN
		cmdExecutor(level := 1, idx := 7, percent := gDev.grd[7].ctrl.exPct);
	END_IF
	IF gDev.grd[7].vector = TargetDirect.retract THEN
		cmdExecutor(level := 1, idx := 7, percent := -gDev.grd[7].ctrl.rtPct);
	END_IF
END_IF	
IF NOT gDev.sky[7].ctrl.isError THEN
	IF gDev.sky[7].vector = TargetDirect.extend THEN
		cmdExecutor(level := 2, idx := 7, percent := gDev.sky[7].ctrl.exPct);
	END_IF
	IF gDev.sky[7].vector = TargetDirect.retract THEN
		cmdExecutor(level := 2, idx := 7, percent := -gDev.sky[7].ctrl.rtPct);
	END_IF
END_IF
*)


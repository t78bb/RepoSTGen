METHOD manualExecute
VAR_INPUT
END_VAR
VAR
	//targetDirect		:TargetDirect;
END_VAR

FOR gi := 1 TO 10 DO
	IF gUI.grd[gi].pwrEnable THEN
		cmdExecutor0(level := 1, idx := gi, 
					direct := gDev.grd[gi].vector, 
					percent := gUI.grd[gi].pwrPercent);
	ELSE
		cmdExecutor0(level := 1, idx := gi, direct := 3, percent := 0);		
	END_IF
END_FOR

FOR si := 0 TO 10 DO
	IF gUI.sky[si].pwrEnable THEN
		cmdExecutor0(level := 2, idx := si, 
					direct := gDev.sky[si].vector, 
					percent := gUI.sky[si].pwrPercent);	
	ELSE
		cmdExecutor0(level := 2, idx := si, direct := 3, percent := 0);		
	END_IF
END_FOR


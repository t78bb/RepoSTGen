//位移值及伸出百分比参数输出	
FOR gi := 1 TO 10 DO
	gUI.grd[gi].postion := gDev.grd[gi].sensor.position;
	gUI.grd[gi].speed := gDev.grd[gi].sensor.speed;
	gUI.grd[gi].extendPercent := percentCalc(1, gi);
END_FOR
FOR si := 0 TO 10 DO
	gUI.sky[si].postion := gDev.sky[si].sensor.position;
	gUI.sky[si].speed := gDev.sky[si].sensor.speed;
	gUI.sky[si].extendPercent := percentCalc(2, si);
END_FOR


//模式判断
pidMode := gUI.mode.usePID;
autoEnableMode := gUI.mode.autoEnable;
autoButtonMode := NOT gUI.mode.manualButtonSet;
autoPctMode := NOT gUI.mode.manualPercentSet;
manualPidPrmSet := gUI.mode.manualSetPid;
//command generetor
FOR gi := 1 TO 10 DO
	IF gUI.grd[gi].btnExtend <> gUI.grd[gi].btnRetract THEN
		gDev.grd[gi].state := DevStatus.runing;
		IF gUI.grd[gi].btnExtend THEN
			gDev.grd[gi].vector := TargetDirect.extend;
			gUI.grd[gi].btnLast := TargetDirect.extend;
		END_IF
		IF gUI.grd[gi].btnRetract THEN
			gDev.grd[gi].vector := TargetDirect.retract;
			gUI.grd[gi].btnLast := TargetDirect.retract;			
		END_IF
	ELSE
		IF gUI.grd[gi].btnExtend THEN
			//伸缩指令不能同时发出，检测到后进行动作转换，重置计数器
			gDev.grd[gi].timeCounter := 0;
			gDev.grd[gi].exeCounter := 0;
			IF gUI.grd[gi].btnLast = TargetDirect.retract THEN
				gDev.grd[gi].vector := TargetDirect.extend;
			ELSE
				gDev.grd[gi].vector := TargetDirect.retract;
			END_IF
			setButtonByDirect(1, gi, gDev.grd[gi].vector);
		ELSE
			gDev.grd[gi].vector := TargetDirect.stop;	
		END_IF
	END_IF
	IF gUI.grd[gi].btnStop THEN
		gDev.grd[gi].vector := TargetDirect.stop;
		setButtonByDirect(1, gi, gDev.grd[gi].vector);
	END_IF
END_FOR

FOR si := 0 TO 10 DO
	IF gUI.sky[si].btnExtend <> gUI.sky[si].btnRetract THEN
		gDev.sky[si].state := DevStatus.runing;
		IF gUI.sky[si].btnExtend THEN
			gDev.sky[si].vector := TargetDirect.extend;
			gUI.sky[si].btnLast := TargetDirect.extend;
		END_IF
		IF gUI.sky[si].btnRetract THEN
			gDev.sky[si].vector := TargetDirect.retract;
			gUI.sky[si].btnLast := TargetDirect.retract;			
		END_IF
	ELSE
		IF gUI.sky[si].btnExtend THEN
			//伸缩指令不能同时发出，检测到后进行动作转换，重置计数器
			gDev.sky[si].timeCounter := 0;
			gDev.sky[si].exeCounter := 0;
			IF gUI.sky[si].btnLast = TargetDirect.retract THEN
				gDev.sky[si].vector := TargetDirect.extend;
			ELSE
				gDev.sky[si].vector := TargetDirect.retract;
			END_IF
			setButtonByDirect(2, si, gDev.sky[si].vector);
		ELSE
			gDev.sky[si].vector := TargetDirect.stop;
		END_IF
	END_IF
	IF gUI.sky[si].btnStop THEN
		gDev.sky[si].vector := TargetDirect.stop;
		setButtonByDirect(1, gi, gDev.grd[gi].vector);
	END_IF
END_FOR


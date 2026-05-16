FOR gi := 1 TO 10 DO
	IF gUI.grd[gi].btnExtend THEN
		gUI.grd[gi].pwrPercent := gDev.grd[gi].ctrl.exPct;
	END_IF
	IF gUI.grd[gi].btnRetract THEN
		gUI.grd[gi].pwrPercent := gDev.grd[gi].ctrl.rtPct;
	END_IF
END_FOR

FOR si := 0 TO 10 DO
	IF gUI.sky[si].btnExtend THEN
		gUI.sky[si].pwrPercent := gDev.sky[si].ctrl.exPct;
	END_IF
	IF gUI.sky[si].btnRetract THEN
		gUI.sky[si].pwrPercent := gDev.sky[si].ctrl.rtPct;
	END_IF
END_FOR

//grd[5]比例输出特判(延时时间过长，小信号无法动作，动作后速度过快的问题)使用速度传感器判定
IF gUI.grd[5].btnExtend THEN 
	IF ABS(gDev.grd[5].sensor.extendVal - gDev.grd[5].sensor.position) < 25 THEN
		gUI.grd[5].pwrPercent := 22;	
	END_IF
END_IF
IF gUI.grd[5].btnRetract THEN 
	IF ABS(gDev.grd[5].sensor.retractVal - gDev.grd[5].sensor.position) < 30 THEN
		gUI.grd[5].pwrPercent := 22;	
	END_IF
END_IF

//其他特判
(*IF gUI.grd[2].btnRetract THEN 
	IF ABS(gDev.grd[2].sensor.retractVal - gDev.grd[2].sensor.position) < 20 THEN
		gUI.grd[2].pwrPercent := 21;	
	END_IFa
END_IF*)
IF gUI.grd[6].btnRetract THEN 
	IF ABS(gDev.grd[6].sensor.retractVal - gDev.grd[6].sensor.position) < 25 THEN
		gUI.grd[6].pwrPercent := 21;	
	END_IF
END_IF


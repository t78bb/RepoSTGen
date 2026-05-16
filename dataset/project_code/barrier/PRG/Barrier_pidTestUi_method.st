METHOD pidTestUi
VAR_INPUT
END_VAR

VAR

END_VAR

IF gUI.pid.level = 1 AND gUI.pid.idx = 0 THEN	//地轨从1-10，天轨从0-10
	RETURN;
END_IF

IF gUI.mode.syncExt THEN
	gUI.grd[gUI.pid.idx].btnExtend := TRUE;gUI.sky[gUI.pid.idx].btnExtend := TRUE;
END_IF
IF gUI.mode.syncRct THEN
	gUI.grd[gUI.pid.idx].btnRetract := TRUE;gUI.sky[gUI.pid.idx].btnRetract := TRUE;
END_IF

IF (NOT gUI.pid.posBtn) THEN
	RETURN;
END_IF

IF gUI.pid.level = 1 THEN 	//地轨部分
	IF idx = gUI.pid.idx THEN		//标号相同更新设备参数
		
		gUI.pid.devSetPos := gDev.grd[idx].ctrl.pos.Set_Point;
		gUI.pid.executeVal := grdPid[idx].res;
		resetPidParam := gUI.pid.rstPidBtn;
		//-----------------位置环------------------------------//
		gUI.pid.pos.Act_Val := gDev.grd[idx].sensor.position;
		gUI.pid.pos.Err := gUI.pid.pos.Set_Point - gUI.pid.pos.Act_Val;
		gUI.pid.pos.OUT := gDev.grd[idx].ctrl.pos.OUT;
		gDev.grd[idx].ctrl.pos := gUI.pid.pos;
		//-----------------速度环------------------------------//
		gUI.pid.spd.Act_Val := gDev.grd[idx].sensor.speed;
		gUI.pid.spd.Err := gUI.pid.spd.Set_Point - gUI.pid.spd.Act_Val;
		gUI.pid.spd.OUT := gDev.sky[idx].ctrl.spd.OUT;
		gDev.grd[idx].ctrl.spd := gUI.pid.spd;
		//-----------------前馈参数------------------------------//
		gDev.grd[idx].ctrl.ff := gUI.pid.ff;	
		
	ELSE							//标号不同，更新界面参数
		idx := gUI.pid.idx;
		gUI.pid.pos := gDev.grd[idx].ctrl.pos;
		gUI.pid.spd := gDev.grd[idx].ctrl.spd;
		gUI.pid.ff	:= gDev.grd[idx].ctrl.ff;	
	END_IF			
END_IF
IF gUI.pid.level = 2 THEN 					//天轨部分
	IF idx = gUI.pid.idx THEN		//标号相同更新设备参数
		
		//-----------------位置环------------------------------//
		gUI.pid.pos.Act_Val := gDev.sky[idx].sensor.position;
		gUI.pid.pos.Err := gUI.pid.pos.Set_Point - gUI.pid.pos.Act_Val;
		gUI.pid.pos.OUT := gDev.sky[idx].ctrl.pos.OUT;
		gDev.sky[idx].ctrl.pos := gUI.pid.pos;
		//-----------------速度环------------------------------//
		gUI.pid.spd.Act_Val := gDev.sky[idx].sensor.speed;
		gUI.pid.spd.Err := gUI.pid.spd.Set_Point - gUI.pid.spd.Act_Val;
		gUI.pid.spd.OUT := gDev.sky[idx].ctrl.spd.OUT;
		gDev.sky[idx].ctrl.spd := gUI.pid.spd;
		//-----------------前馈参数------------------------------//
		gDev.sky[idx].ctrl.ff := gUI.pid.ff;	

		gUI.pid.devSetPos := gDev.sky[idx].ctrl.pos.Set_Point;
		gUI.pid.executeVal := skyPid[idx].res;
		resetPidParam := gUI.pid.rstPidBtn;

	ELSE							//标号不同，更新界面参数
		idx := gUI.pid.idx;
		gUI.pid.pos := gDev.sky[idx].ctrl.pos;
		gUI.pid.spd := gDev.sky[idx].ctrl.spd;
		gUI.pid.ff	:= gDev.sky[idx].ctrl.ff;

	END_IF			

END_IF
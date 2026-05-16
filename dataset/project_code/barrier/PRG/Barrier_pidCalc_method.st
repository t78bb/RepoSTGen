METHOD pidCalc
VAR_INPUT
END_VAR
VAR
	vector			:TargetDirect;
END_VAR

FOR gi := 1 TO 10 DO
	IF NOT manualPidPrmSet THEN
		vector := gDev.grd[gi].vector;
		CASE vector OF
			TargetDirect.stop:
			CASE gDev.grd[gi].state OF
				DevStatus.extended:
					gDev.grd[gi].ctrl.pos.Set_Point := gDev.grd[gi].ctrl.extVal;
				DevStatus.retracted:
					gDev.grd[gi].ctrl.pos.Set_Point := gDev.grd[gi].ctrl.rtcVal;
				ELSE
					gDev.grd[gi].ctrl.pos.Set_Point := gDev.grd[gi].sensor.position;
			END_CASE			
			TargetDirect.extend:
				gDev.grd[gi].ctrl.pos.Set_Point := gDev.grd[gi].ctrl.extVal;
			TargetDirect.retract:
				gDev.grd[gi].ctrl.pos.Set_Point := gDev.grd[gi].ctrl.rtcVal;
		END_CASE
END_IF
	
	grdPid[gi](idx := gi, isReset := resetPidParam, cycTimer := 0.01, res => );

END_FOR

FOR si := 0 TO 10 DO
	IF NOT manualPidPrmSet THEN
		vector := gDev.sky[si].vector;
		CASE vector OF
			TargetDirect.stop:
			CASE gDev.sky[si].state OF
				DevStatus.extended:
					gDev.sky[si].ctrl.pos.Set_Point := gDev.sky[si].ctrl.extVal;
				DevStatus.retracted:
					gDev.sky[si].ctrl.pos.Set_Point := gDev.sky[si].ctrl.rtcVal;
				ELSE
					gDev.sky[si].ctrl.pos.Set_Point := gDev.sky[si].sensor.position;
			END_CASE			
			TargetDirect.extend:
				gDev.sky[si].ctrl.pos.Set_Point := gDev.sky[si].ctrl.extVal;
			TargetDirect.retract:
				gDev.sky[si].ctrl.pos.Set_Point := gDev.sky[si].ctrl.rtcVal;
		END_CASE
		
		
	END_IF
	skyPid[si](idx := si, isReset := resetPidParam, cycTimer := 0.01, res =>);
END_FOR


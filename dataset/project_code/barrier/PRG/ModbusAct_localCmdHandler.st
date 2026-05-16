METHOD localCmdHandler
VAR_INPUT
END_VAR
VAR
	iBit				:INT;
	exLevel				:INT;
	exIdx				:INT;
	exDirect			:TargetDirect;
	exeDirect			:TargetDirect;

END_VAR
VAR CONSTANT
	no		:ARRAY [1..8] OF INT :=[11, 14, 17, 20, 49, 50, 51, 52];	
END_VAR


FOR iSec := 1 TO 8 DO
	gModbus.srv.request.data[no[iSec]] := gModbus.modbusBuffer[no[iSec]];
END_FOR

FOR iSec := 1 TO 4 DO
	gModbus.srv.request.arrNew[iSec,1	] := gModbus.srv.request.data[no[iSec]].1	;
	gModbus.srv.request.arrNew[iSec,2	] := gModbus.srv.request.data[no[iSec]].2	;
	gModbus.srv.request.arrNew[iSec,3	] := gModbus.srv.request.data[no[iSec]].3	;
	gModbus.srv.request.arrNew[iSec,4	] := gModbus.srv.request.data[no[iSec]].4	;
	gModbus.srv.request.arrNew[iSec,5	] := gModbus.srv.request.data[no[iSec]].5	;
	gModbus.srv.request.arrNew[iSec,6	] := gModbus.srv.request.data[no[iSec]].6	;
	gModbus.srv.request.arrNew[iSec,7	] := gModbus.srv.request.data[no[iSec]].7	;
	gModbus.srv.request.arrNew[iSec,8	] := gModbus.srv.request.data[no[iSec]].8	;
	gModbus.srv.request.arrNew[iSec,9	] := gModbus.srv.request.data[no[iSec]].9	;
	gModbus.srv.request.arrNew[iSec,10	] := gModbus.srv.request.data[no[iSec]].10	;
	gModbus.srv.request.arrNew[iSec,11	] := gModbus.srv.request.data[no[iSec]].11	;
END_FOR
FOR iSec := 1 TO 4 DO
	FOR iBit := 1 TO 11 DO
		IF gModbus.srv.request.arrNew[iSec, iBit] <> gModbus.srv.request.arrLast[iSec, iBit] THEN
			IF gModbus.srv.request.arrNew[iSec, iBit] THEN	//仅执行上升沿
				//specifically output[grd/sky(exLevel), no(exIdx), TargetDirect(exDirect)]
				l2p(section := iSec, lgcIdx := iBit, 
					level => exLevel, phyIdx => exIdx, direct => exDirect);
				exeDirect := rvs.cmdReverse(input := exDirect);		//华中要求伸缩指令及状态翻转
				
				//过滤	机械结构未完成的grd[4] and sky[4]
				IF exIdx = 4 THEN	exeDirect := TargetDirect.stop;	END_IF
				
				setButtonByDirect(level := exLevel, idx := exIdx, direct := exeDirect);
			END_IF
			gModbus.srv.request.arrLast[iSec, iBit] := gModbus.srv.request.arrNew[iSec, iBit];			
		END_IF
	END_FOR
	
END_FOR


devNum := gModbus.modbusBuffer[49];


//新增一键启动液压站

IF gUI.mode.hydPowerOn THEN
	holdingBuff[48] := holdingBuff[48] OR 1;
END_IF
IF gUI.mode.hydPowerOff THEN
	holdingBuff[48] := holdingBuff[48] OR 2;
END_IF


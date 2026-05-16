METHOD localStatHandler : TargetDirect
VAR_INPUT
END_VAR


//先把天地轨控制器数据同步至本地
FOR idx := 110 TO 319 DO
	gModbus.srv.response.data[idx] := holdingBuff[idx];
END_FOR

//根据实际状态将挡板数据同步至本地
FOR gi := 1 TO 10 DO
	(*******************************
	伸缩反向判定，伸出到位返回缩回到位
	**********************************)
	
	//地轨伸出到位检查
	p2l(section := 1, phyIdx := gi, lgcIdx => logicIdx);//logicIdx范围[223,232]
	IF gDev.grd[gi].state = DevStatus.retracted THEN
		gModbus.srv.response.data[logicIdx] := 1;
	ELSE
		gModbus.srv.response.data[logicIdx] := 0;
	END_IF
	//地轨缩回到位检查
	p2l(section := 2, phyIdx := gi, lgcIdx => logicIdx);//logicIdx范围[271,280]
	IF gDev.grd[gi].state = DevStatus.extended THEN
		gModbus.srv.response.data[logicIdx] := 1;
	ELSE
		gModbus.srv.response.data[logicIdx] := 0;
	END_IF
END_FOR

FOR si := 0 TO 10 DO
	//天轨伸出到位检查
	p2l(section := 3, phyIdx := si, lgcIdx => logicIdx);//logicIdx范围[127,137]
	
	
	IF gDev.sky[si].state = DevStatus.retracted THEN
		gModbus.srv.response.data[logicIdx] := 1;
	ELSE
		gModbus.srv.response.data[logicIdx] := 0;
	END_IF
	//天轨缩回到位检查
	p2l(section := 4, phyIdx := si, lgcIdx => logicIdx);//logicIdx范围[175,185]
	IF gDev.sky[si].state = DevStatus.extended THEN
		gModbus.srv.response.data[logicIdx] := 1;
	ELSE
		gModbus.srv.response.data[logicIdx] := 0;
	END_IF	
END_FOR
//至此110-309寄存器状态更新完毕，向华中发送时只需在寄存器写入response.data[]数组

IF devNum > 40000 THEN
	n2i(devNo := devNum, level => , idx =>);
	CASE n2i.level OF
		1:
			gModbus.srv.response.data[312] := REAL_TO_WORD(10 * gDev.grd[n2i.idx].sensor.position);
			gModbus.srv.response.data[313] := REAL_TO_WORD(10 * gDev.grd[n2i.idx].sensor.extendVal);
			gModbus.srv.response.data[314] := REAL_TO_WORD(10 * gDev.grd[n2i.idx].sensor.retractVal);
		2:
			gModbus.srv.response.data[312] := REAL_TO_WORD(10 * gDev.sky[n2i.idx].sensor.position);
			gModbus.srv.response.data[313] := REAL_TO_WORD(10 * gDev.sky[n2i.idx].sensor.extendVal);
			gModbus.srv.response.data[314] := REAL_TO_WORD(10 * gDev.sky[n2i.idx].sensor.retractVal);
	END_CASE
END_IF


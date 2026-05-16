FUNCTION percentCalc : REAL
VAR_INPUT
	level		:INT;	//1->地轨	2->天轨
	idx			:INT;	//挡板索引编号
END_VAR
VAR
	c			:REAL;
	p			:REAL;
END_VAR


//伸出百分比计算
CASE level OF
	1:
		IF gDev.grd[idx].sensor.position < 3 THEN 
			RETURN;
		END_IF
		c := gDev.grd[idx].sensor.position - gDev.grd[idx].sensor.retractVal;
		p := gDev.grd[idx].sensor.extendVal - gDev.grd[idx].sensor.retractVal;
		percentCalc := c * 100 / p;
	2:
		IF gDev.sky[idx].sensor.position < 3 THEN 
			RETURN;
		END_IF
		c := gDev.sky[idx].sensor.position - gDev.sky[idx].sensor.retractVal;
		p := gDev.sky[idx].sensor.extendVal - gDev.sky[idx].sensor.retractVal;
		percentCalc := c * 100 / p;
END_CASE

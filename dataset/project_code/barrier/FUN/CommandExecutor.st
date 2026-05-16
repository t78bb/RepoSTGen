
FUNCTION_BLOCK CommandExecutor
VAR_INPUT
	level		:INT;			//1->地轨	2->天轨
	idx			:INT;			//挡板索引编号
	percent		:REAL;			//比例阀百分比 传入-100~+100
END_VAR
VAR_OUTPUT
END_VAR
VAR
END_VAR

IF percent > 0 THEN
	CASE level OF
		1:
			gController.grd[idx].extendPercent := REAL_TO_WORD(percent * 65535 / 100);
			gController.grd[idx].retractPercent := 0;
		2:
			gController.sky[idx].extendPercent := REAL_TO_WORD(percent * 65535 / 100);
			gController.sky[idx].retractPercent := 0;
	END_CASE
ELSE
	CASE level OF
		1:
			gController.grd[idx].extendPercent := 0;
			gController.grd[idx].retractPercent := REAL_TO_WORD(ABS(percent) * 65535 / 100);
		2:
			gController.sky[idx].extendPercent := 0;
			gController.sky[idx].retractPercent := REAL_TO_WORD(ABS(percent) * 65535 / 100);
	END_CASE
END_IF
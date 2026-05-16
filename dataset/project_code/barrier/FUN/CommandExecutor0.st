FUNCTION_BLOCK CommandExecutor0
VAR_INPUT
	level		:INT;			//1->地轨	2->天轨
	idx			:INT;			//挡板索引编号
	direct		:TargetDirect;	//方向
	percent		:REAL;			//比例阀百分比 传入0-100
END_VAR
VAR_OUTPUT
END_VAR
VAR
END_VAR

CASE direct OF
	TargetDirect.extend:
		CASE level OF
			1:
				gController.grd[idx].extendPercent := REAL_TO_WORD(percent * 65535 / 100);
				gController.grd[idx].retractPercent := 0;
			2:
				gController.sky[idx].extendPercent := REAL_TO_WORD(percent * 65535 / 100);
				gController.sky[idx].retractPercent := 0;
		END_CASE
	TargetDirect.retract:
		CASE level OF
			1:
				gController.grd[idx].extendPercent := 0;
				gController.grd[idx].retractPercent := REAL_TO_WORD(percent * 65535 / 100);
			2:
				gController.sky[idx].extendPercent := 0;
				gController.sky[idx].retractPercent := REAL_TO_WORD(percent * 65535 / 100);
		END_CASE
	TargetDirect.stop:
		CASE level OF
			1:
				gController.grd[idx].extendPercent := 0;
				gController.grd[idx].retractPercent := 0;
			2:
				gController.sky[idx].extendPercent := 0;
				gController.sky[idx].retractPercent := 0;
		END_CASE
	
	ELSE
		CASE level OF
			1:
				gController.grd[idx].extendPercent := 0;
				gController.grd[idx].retractPercent := 0;
			2:
				gController.sky[idx].extendPercent := 0;
				gController.sky[idx].retractPercent := 0;
		END_CASE
		
END_CASE

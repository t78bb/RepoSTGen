FUNCTION setButtonByDirect : BOOL
VAR_INPUT
	level		:INT;	//1->地轨	2->天轨
	idx			:INT;	//挡板索引编号
	direct		:TargetDirect;
END_VAR
VAR
END_VAR
//	本函数用于根据输入参数 操作UI界面的按钮变量
CASE level OF
	1:
		IF idx = 0 OR idx > 10 THEN		//参数校验
			RETURN;
		END_IF
		CASE direct OF
			TargetDirect.extend:
				gUI.grd[idx].btnStop := FALSE;
				gUI.grd[idx].btnExtend := TRUE;
				gUI.grd[idx].btnRetract := FALSE;
			TargetDirect.retract:
				gUI.grd[idx].btnStop := FALSE;
				gUI.grd[idx].btnExtend := FALSE;
				gUI.grd[idx].btnRetract := TRUE;
			TargetDirect.stop:
				gUI.grd[idx].btnStop := FALSE;
				gUI.grd[idx].btnExtend := FALSE;
				gUI.grd[idx].btnRetract := FALSE;
		END_CASE
	2:
		IF idx > 10 THEN		//参数校验
			RETURN;
		END_IF
		CASE direct OF
			TargetDirect.extend:
				gUI.sky[idx].btnStop := FALSE;
				gUI.sky[idx].btnExtend := TRUE;
				gUI.sky[idx].btnRetract := FALSE;
			TargetDirect.retract:
				gUI.sky[idx].btnStop := FALSE;
				gUI.sky[idx].btnExtend := FALSE;
				gUI.sky[idx].btnRetract := TRUE;
			TargetDirect.stop:
				gUI.sky[idx].btnStop := FALSE;
				gUI.sky[idx].btnExtend := FALSE;
				gUI.sky[idx].btnRetract := FALSE;
		END_CASE
		
END_CASE;
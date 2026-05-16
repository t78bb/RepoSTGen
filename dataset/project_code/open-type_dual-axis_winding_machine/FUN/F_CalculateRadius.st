FUNCTION F_CalculateRadius : LREAL
VAR_INPUT
	lD				:	LREAL;		//两轴中心距离
	lHold			:	LREAL;		//测量开始时的AxisV位置
	lHnew			:	LREAL;		//测量结束时的AxisV位置
	lTk				:	LREAL;		//材料厚度
	lOffset			:	LREAL;		//高度偏移量
END_VAR

// 半径计算公式：
// R = |√(D²+(Hnew+offset)²) - √(D²+(Hold+offset)²)| / π + Tk
F_CalculateRadius := ABS(SQRT(EXPT(lD,2)+EXPT(lHnew+lOffset,2)) - SQRT(EXPT(lD,2)+EXPT(lHold+lOffset,2))) / SMC_PI + lTk;


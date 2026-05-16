PROGRAM RunReset
VAR
	fbDualReset		:	FB_DualAxisReset;	//双轴复位功能块
	bExecuteReset	:	BOOL := TRUE;		//自动执行复位
END_VAR
VAR_OUTPUT
	bDone			:	BOOL;
END_VAR

// 使用双轴复位功能块
fbDualReset(
	Axis1 := AxisX,
	Axis2 := AxisY,
	bExecute := bExecuteReset
);

// 输出复位完成状态
bDone := fbDualReset.bDone;

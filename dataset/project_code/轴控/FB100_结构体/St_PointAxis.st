TYPE St_PointAxis ://轴结构体参数
STRUCT
	//输入
	i_xReset			: BOOL;//轴复位
	i_xSerOn			: BOOL;//轴使能
	i_xStop				: BOOL;//轴停止
	i_xHalt             : BOOL;//轴暂停
	i_xHome				: BOOL;//轴回原
	i_xJogP				: BOOL;//轴正向点动
	i_xJogN				: BOOL;//轴反向点动
	i_xGoAbs			: BOOL;//轴绝对位置
	i_xGoRel			: BOOL;//轴相对位置
	i_xGoVel			: BOOL;//轴速度模式
	i_xSetPos			: BOOL;//轴位置设定
	i_xFolPos			: BOOL;//轴位置设定
	
	i_iGoAbs_dir		: INT;//轴运动方向
	i_xVirtual			: BOOL;//虚轴开关
	i_fAxisAcc			: LREAL;//轴加速度
	i_fAxisDec			: LREAL;//轴减速度
	i_fJogVel			: LREAL;//轴点动速度
	i_fHome_Pos			: LREAL;//轴回原偏置
	i_fGoAbs_Pos		: LREAL;//轴绝对定位位置
	i_fGoAbs_Vel		: LREAL;//轴绝对定位速度
	i_fGoRel_Pos		: LREAL;//轴相对定位位置
	i_fGoRel_Vel		: LREAL;//轴相对定位速度
	i_fGoVel_Vel		: LREAL;//轴速度模式速度
	i_fSetPos_Pos		: LREAL;//轴设定位置
	i_fFolPos_Pos		: LREAL;
	//输出
	o_xFbErr			: BOOL;//轴控功能块报错
	o_xFbBusy			: BOOL;//轴控功能块运行中
	o_xFbDone			: BOOL;//轴控功能块完成
	o_iFbErrID			: UDINT;//轴控功能块报错ID
	o_xAxisErr			: BOOL;//轴故障
	o_xAxisStand		: BOOL;//轴等待
	o_xAxisRun			: BOOL;//轴运行中
	o_iAxisState		: INT;//轴状态机
	o_xDriveRdy			: BOOL;//站待机
	o_xDriveRN			: BOOL;//站运行
	o_xDriveErr			: BOOL;//站报错
	o_xDriveAlarm		: BOOL;//站警报
	o_xPositiveLimit	: BOOL;//轴正限位
	o_xNegativeLimit	: BOOL;//轴负限位
	o_xHomeSwitch		: BOOL;//轴原点开关
	o_fActVel			: LREAL;//轴实际速度
	o_fActPos			: LREAL;//轴实际位置
	o_fActTor			: LREAL;//轴实际转矩
	o_xResetDone		: BOOL;//轴复位完成
	o_xResetErr         : BOOL;//轴复位失败
	
	//指针
	pAxis				: POINTER TO AXIS_REF_ETC_DS402_CS;//轴地址
	pServer				: POINTER TO ETCSlave;//站地址
END_STRUCT
END_TYPE
TYPE UiPid :
STRUCT
	pos				:PidParam;			//位置pid参数
	spd				:PidParam;			//速度pid参数
	ff				:FeedForward;		//前馈参数

	level			:INT;				//1->地轨	2->天轨
	idx				:INT;				//挡板索引编号
	
	devSetPos		:REAL;				//设备中的设定位置点(用于观测)
	executeVal		:REAL;				//执行值(-100.0~+100.0)

	
	posBtn			:BOOL;			//位置控制按钮，按下实时更新交互参数
	rstPidBtn		:BOOL;			//reset pid param button重置pid参数按钮
	pwrPercent		:REAL;			//比例阀百分比 power-percent 0-100	
	
	
	
	
	extendBtn		:BOOL;
	retractBtn		:BOOL;
	stopBtn			:BOOL;


	
	
(*	posErr			:REAL;
	posOut			:REAL;
	spdErr			:REAL;
	spdOut			:REAL;*)	
END_STRUCT
END_TYPE

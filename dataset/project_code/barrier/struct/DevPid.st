TYPE DevPid :
STRUCT
	pos			:PidParam;			//位置pid参数
	spd			:PidParam;			//速度pid参数
	ff			:FeedForward;		//前馈参数
//	dp			:DynamicPlanning;	//规划参数
	exPct		:REAL;				//伸出默认比例量0-100
	rtPct		:REAL;				//缩回默认比例量0-100
	
	isError		:BOOL;				//当传感器数据为0时，报错并不执行pid
	
	extVal		:REAL;				//设定伸出位移值
	rtcVal		:REAL;				//设定缩回位移值
	
END_STRUCT
END_TYPE

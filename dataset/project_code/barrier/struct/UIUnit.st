TYPE UIUnit :
STRUCT
	//cmd
	pwrEnable			:BOOL;		//比例阀使能   power-enable
	pwrPercent			:REAL;		//比例阀百分比 power-percent 0-100
	
	//button
	btnExtend			:BOOL;
	btnRetract			:BOOL;
	btnStop				:BOOL;
	btnLast				:TargetDirect;	//上次动作方向
	
	//info display
	name				:STRING;	//挡板名
	wname				:WSTRING;	//山河命名
	hzname				:WSTRING;	//hua zhong ming ming
	postion				:REAL;		//位移值
	speed				:REAL;
	extendPercent		:REAL;		//伸出百分比 extend-percent
	
	
	
END_STRUCT
END_TYPE

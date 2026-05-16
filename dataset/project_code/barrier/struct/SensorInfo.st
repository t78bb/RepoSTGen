TYPE SensorInfo :
STRUCT
	
	position	:REAL;	//实时位移
	speed		:REAL;	//实时速度
	
	//记录最大最小位移值
	retractVal	:REAL;	//缩回到位值
	extendVal	:REAL;	//伸出到位值
	
END_STRUCT
END_TYPE

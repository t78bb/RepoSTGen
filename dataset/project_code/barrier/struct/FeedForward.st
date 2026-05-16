TYPE FeedForward :
STRUCT
	
	pstThreshold	:REAL;	//正向设定阈值	
	pstKv			:REAL;
	pstKa			:REAL;
	pstKaa			:REAL;
	negThreshold	:REAL;	//反向设定阈值
	negKv			:REAL;
	negKa			:REAL;
	negKaa			:REAL;
	

	
//	pstFactor		:REAL;	//正向设定速度系数因子
//	negFactor		:REAL;	//反向设定速度系数因子


END_STRUCT
END_TYPE

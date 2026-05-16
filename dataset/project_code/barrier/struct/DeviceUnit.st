TYPE DeviceUnit :
STRUCT
		
	sensor			:SensorInfo;		//传感器参数
	ctrl			:DevPid;			//pid等计算控制执行参数	
	
	vector			:TargetDirect;		//指令运行方向 1-伸出 2-缩回 3-停止
	state			:DevStatus;			//设备状态 0-未知 1-运行 2-伸出到位 3-缩回到位 4-错误
	
	timeCounter		:INT;				//timeoutCounter超时计数器
	exeCounter		:INT;				//ExecuteCounter额外执行时间计数

	current			:ARRAY[1..2] OF WORD;	//电流mA	[i,j] -> 地轨挡板i的电流，j=1伸出电流，j=2缩回电流


END_STRUCT
END_TYPE

VAR_GLOBAL
	
	sFileName: STRING := 'I:\test.txt';	//G代码文件名
	sSystem_Error: STRING(100);					//系统错误

	dwSystem_Error: DWORD :=0;				//系统错误代码
	dwIpoCycTime: DWORD := 10000;			//插补循环周期
	
	fOverride: LREAL := 100;				//进给倍率
	
	fHomeVelocitySlow: LREAL := 50;			//慢速回零
	fHomeVelocityFast: LREAL := 100;		//快速回零
	fHomeAcceleration: LREAL := 20;			//回零加速度
	fHomeDeceleration: LREAL := 40;			//回零减速度
	fAxisX_Offset: LREAL;					//X轴坐标偏移
	fAxisY_Offset: LREAL;					//Y轴坐标偏移
	fAxisZ_Offset: LREAL;					//Z轴坐标偏移
	
	bAxisXReferenceSwitch: BOOL :=TRUE;		//X轴机械零点
	bAxisYReferenceSwitch: BOOL :=TRUE;		//Y轴机械零点
	bAxisZReferenceSwitch: BOOL :=TRUE;		//Z轴机械零点

	Act_Gline:LREAL:=0;
END_VAR
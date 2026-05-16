VAR_GLOBAL
	IOri	:	BOOL;	//原点开关
	LFlage:BOOL;	//左限位开关
	RFlage:BOOL;	//右限位开关
	IReset	:	BOOL;	//复位
	IStop	:	BOOL;	//停止
	IEStop	:	BOOL;	//急停
	IRun	:	BOOL;	//启动
	
	QLedY	:	BOOL:=TRUE;
	QLedR	:	BOOL;
	QLedG	:	BOOL;
	
	MHmiInHomeVel	:	LREAL:=20;	//回零速度
	MHmiInJogVel	:	LREAL:=25;	//点动速度
	MHmiInVel	:	LREAL:=20;	//初始速度
	MHmiInG	:	LREAL:=0.7;	//浮棍重量
	MHmiOutF		:	LREAL;	//实时拉力
	MHmiAxisVPos	:	REAL;
	MHmiOutModeNo		:	USINT;//工作模式ID
	
	MHmiJogMP	:	BOOL;	//M轴正向点动
	MHmiJogMN	:	BOOL;	//M轴负向点动
	MHmiJogSP	:	BOOL;	//S轴正向点动
	MHmiJogSN	:	BOOL;	//S轴负向点动
	MHmiModeChange	:	BOOL;	//自动手动模式切换按钮
	
	MHmiLed1,MHmiLed2,MHmiLed3,MHmiLed4	:	BOOL;
	MHmiLGo,MHmiRGo	:	BOOL;
	
	AxisMSta	:	AxisStatus;
	AxisSSta	:	AxisStatus;
	MHmiOutMessage	:	STRING;
END_VAR
PROGRAM ModbusAct
VAR
	bInit					: BOOL:=TRUE;
	iCountAct				: UINT:=10;	
	connectStatus			: UINT;
	iErrCode				: BYTE;
	idx						: INT;
	logicIdx				: INT;
	gi						: INT;
	si						: INT;		
	iSec					: INT;		//section iterator
	devNum					: WORD;
	fbModbusServer			: ModbusServer;
	inputBuff				: ARRAY[0..1000]OF WORD;
	holdingBuff				: ARRAY[0..1000]OF WORD;
	
	fbModbusClient			: ModbusTcp_Client;
	fbReadHoldRegister  	: ReadHoldRegister;		//读保持寄存器
	fbWriteMutiRegister		: WriteMutiRegister;	
	l2p						: mdbsLogicToPhy;
	p2l						: mdbsPhyToLogic;
	n2i						: mdbsNumToIdx;
	rvs						: DataReverse;
END_VAR

//初始化
IF bInit THEN
	initialize();
	bInit := FALSE;
END_IF

IF connectStatus <> 1 THEN
	fbModbusClient(sIPAddress:='192.168.2.21',uiPort:=520);//连接IPC
	//fbModbusClient(sIPAddress:='192.168.5.55',uiPort:=502);//连接工控机
END_IF

IF fbModbusClient.bSuccess THEN
	connectStatus := 1;	
	CASE iCountAct OF
		10:
			handleCmd();		//接收华中指令
			localCmdHandler();	//处理本机挡板指令 + 启动液压站
		20:
			handleStat1();		//发送状态至华中
		21:
			handleStat2();
		22:
			handleStat3();
	END_CASE
END_IF
		
//做服务器接收天地轨客户端发送的数据
fbModbusServer(	wPort := 512, 
	pInputData := ADR(inputBuff[0]), pOutputData := ADR(holdingBuff[0]), 
	uiInputDataSize := 1000, uiOutputDataSize := 1000, 
	xEnable := TRUE, xReset := FALSE, tTimeout := 1000, 
	xBusy => , xError => , byClientConnections => );


//将缓冲区Buff数据转至本地
localStatHandler();
//updateStat();


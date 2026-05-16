PROGRAM Barrier
VAR
	bInit			:BOOL:=TRUE;
	initCount		:INT:= 100 * 2;		//2s后开始初始化，执行
	timeout			:INT:= 100 * 16;	//10ms间隔时 is 15 second
	timeexe			:INT:= 100 * 8;		//需要停止时，额外执行指令时间
	cmdExecutor0	:CommandExecutor0;
	cmdExecutor		:CommandExecutor;
	grdPid			:ARRAY[1..10] OF grdPosCtrl;
	skyPid			:ARRAY[0..10] OF skyPosCtrl;
	resetPidParam	:BOOL;							//pid参数复位
	pidMode			:BOOL;							//使用pid控制
	autoButtonMode	:BOOL;							//手动复位按钮
	autoEnableMode	:BOOL;							//有动作时使能自动开启
	autoPctMode		:BOOL;
	manualPidPrmSet	:BOOL;							//manualPidParamSet,手动设定pid位置参数

	gi				:INT;			//ground-i
	si				:INT;			//sky-i

	level			:INT;			//1->地轨	2->天轨
	idx				:INT := -1 ;	//挡板索引编号
END_VAR

//初始化
IF initCount = 0 THEN
	IF bInit THEN
		initialize();
		initializePid();
		bInit := FALSE;
	END_IF
ELSE
	initCount := initCount - 1;
	RETURN;	
END_IF

//指令执行
pidTestUi();

IF pidMode THEN
	pidCalc();
	pidExecute();
ELSE
	IF autoPctMode THEN setExecutePercent(); END_IF
	manualExecute();
END_IF	

//界面交互  
interfaceAct();

//状态更新
updateStatus(error := 1);

//复位按钮模式/
IF autoButtonMode THEN
	autoResetButton();
END_IF
IF autoEnableMode THEN
	autoEnable();
END_IF
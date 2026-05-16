PROGRAM Cam
VAR
	fbResetAxis	:	ResetAxis;// 实例化ResetAxis，用来使主从轴复位
	fbCamTableSelect	:	MC_CamTableSelect;// 实例化MC_CamTableSelect
	fbCamIn	:	MC_CamIn;// 实例化MC_CamIn，用来主从耦合
	fbCamOut	:	MC_CamOut;// 实例化MC_CamOut，用来解耦合
	fbMoveRel	:	MC_MoveRelative;// 实例化MC_MoveRelative
	fbMasterMoveVel	:	MC_MoveVelocity;// 实例化MC_MoveVelocity，用来控制主轴的运动
	fbSlaveMoveVel	:	MC_MoveVelocity;// 实例化MC_MoveVelocity，用来控制从轴的运动
	fbMasterHalt	:	MC_Halt;// 实例化MC_Halt，用来控制主轴停止
	fbSlaveHalt	:	MC_Halt;// 实例化MC_Halt，用来控制从轴停止
	
	fbSetActPos1	:	MC_SetPosition;//用来设置主轴当前位置
	fbSetActPos2	:	MC_SetPosition;//用来设置从轴当前位置
	
	bMasterStop	:	BOOL;//控制主轴停止运动，与视图中主轴停止按钮相关联
	bSlaveStop	:	BOOL;//控制从轴停止运动，与视图中从轴停止按钮相关联
	bMasterRun	:	BOOL;//控制主轴开始运动，与视图中主轴起动按钮相关联
	bSlaveRun	:	BOOL;//控制从轴开始运动，与视图中从轴起动按钮相关联
	
	bReset	:	BOOL;//控制整个过程复位
	bGear	:	BOOL;//控制主从轴耦合，与视图中主从耦合按钮相关联
	bGearOut	:	BOOL;//控制主从轴解耦合，与视图中解耦合按钮相关联
	nState	:	BYTE;	
	bIsNeg	:	BOOL;
	str	:	STRING := '';
	fbStopRtrig	:	R_TRIG;
	fbStartRtrig	:	R_TRIG;
	fbResetRtrig	:	R_TRIG;

	fbReadStatusMaster	:	MC_ReadStatus;//实例化MC_ReadStatus，用来读取主轴状态信息
	fbReadStatusSlave	:	MC_ReadStatus;//实例化MC_ReadStatus，用来读取从轴状态信息
	
	//初始化以下四个变量，这四个变量也可以在视图运行过程中，"主轴设定速度:"label后面的Textfield中重新赋值
	masterMotorVel	:	LREAL := 1;//主轴设定速度
	masterMotorAcc	:	LREAL := 20;	
	slaveMotorVel	:	LREAL := 1;//从轴设定速度
	slaveMotorAcc	:	LREAL := 20;

	masterMotorVelTemp	:	LREAL;
	masterMotorAccTemp	:	LREAL;	
	slaveMotorVelTemp	:	LREAL;
	slaveMotorAccTemp	:	LREAL;
	
	bSetMasterActPos	:	BOOL;//与“设置主轴的实际位置为：”button相关联
	bSetSlaveActPos	:	BOOL;//与“设置从轴的实际位置为：”button相关联
	setMasterPos	:	REAL;//与“设置主轴的实际位置为：”button后面的空Textfield相关联
	setSlavePos	:	REAL;//与“设置从轴的实际位置为：”button后面的空Textfield相关联
	
	//以下三个变量用于控制启动模式，即MC_CamIn功能块中的StartMode
	bPeriodic	:	BOOL := TRUE;//与“凸轮周期性执行”button相关联
	bMasterAbs	:	BOOL := TRUE;//与“凸轮主轴位置绝对”button相关联
	bSlaveAbs	:	BOOL := TRUE;//与“凸轮从轴位置绝对”button相关联
	
	masterOff	:	REAL;
	slaveOff	:	REAL;
	masterSca	:	REAL := 1;
	slaveSca	:	REAL := 1;
	
	//以下三个BOOL变量与视图中启动模式下的三个button相关联
	bAbs	:	BOOL := TRUE;//绝对模式
	bRel	:	BOOL;		//相对模式
	bRamp	:	BOOL;
	
	startMode	:	MC_STARTMODE := MC_STARTMODE.absolute;// 定义startMode为absolute，在下面的程序中作为初始化值
	fbRtrig1	:	R_TRIG;
	fbRtrig2	:	R_TRIG;
	fbRtrig3	:	R_TRIG;
	masterStateStr	:	STRING;
	slaveStateStr	:	STRING;
END_VAR

PowerAxis();//调用该函数，使主从轴使能

IF bRunReset AND PowerAxis.bPowerDone THEN
	nState := 0;
	RunReset();
	IF RunReset.bDone THEN
		bRunReset := FALSE;
	END_IF
	RETURN;
END_IF
//为下面四个变量赋初值，在视图中主轴设定速度等处为masterMotorVel等赋值，来相应的改变masterMotorVelTemp等的值，从而控制主从轴的运动
masterMotorVelTemp := masterMotorVel / 60.0 * 360;
masterMotorAccTemp := masterMotorAcc * 360;

slaveMotorVelTemp := slaveMotorVel / 60.0 * 360;
slaveMotorAccTemp := slaveMotorAcc * 360;
//对应在视图中的启动模式（三种）
fbRtrig1(CLK := bAbs);
IF fbRtrig1.Q THEN
	bRel := FALSE;
	bRamp := FALSE;
	startMode := MC_STARTMODE.absolute;//数据类型：MC_StartMODE 0：absolute 绝对位置:1：relative 相对位置: 2：ramp_in ( 斜坡切入) 3：ramp_in_pos（正向斜坡切入）4：ramp_in_neg 反向斜坡切入
END_IF
fbRtrig2(CLK := bRel);
IF fbRtrig2.Q THEN
	bAbs := FALSE;
	bRamp := FALSE;
	startMode := MC_STARTMODE.relative;
END_IF
fbRtrig3(CLK := bRamp);
IF fbRtrig3.Q THEN
	bRel := FALSE;
	bAbs := FALSE;
	startMode := MC_STARTMODE.ramp_in;
END_IF

CASE nState OF
	0:(* 初始化 *)
		fbResetAxis(bExec := TRUE);
		IF fbResetAxis.Done THEN
			fbResetAxis(bExec := FALSE);
			nState := 1;
		END_IF
	1:(* 初始化 *)
		IF PowerAxis.bPowerDone THEN
			fbMasterMoveVel(Execute := FALSE,Axis := AxisX);
			fbSlaveMoveVel(Execute := FALSE,Axis := AxisY);
			fbCamTableSelect(Master := AxisX,Slave := AxisY,CamTable := CamTable,Execute := FALSE);
			fbCamIn(Execute := FALSE,Master := AxisX,Slave := AxisY);
			fbCamOut(Slave := AxisY,Execute := FALSE);	
			fbMasterHalt(Axis := AxisX,Execute := FALSE);
			fbSlaveHalt(Axis := AxisY,Execute := FALSE);
			fbResetAxis(bExec := FALSE);
			fbSetActPos1(Axis := AxisX,Execute := TRUE,Mode := FALSE,Position := 0);
			fbSetActPos2(Axis := AxisY,Execute := TRUE,Mode := FALSE,Position := 0);
			IF fbSetActPos1.Done AND fbSetActPos2.Done THEN
				fbSetActPos1(Axis := AxisX,Execute := FALSE);
				fbSetActPos2(Axis := AxisY,Execute := FALSE);
				nState := 2;
			END_IF
		END_IF
	2:
		fbResetRtrig(CLK := bReset);
		IF fbResetRtrig.Q THEN  //判断是否复位，若复位，则将所有功能置为复位状态
			fbMasterMoveVel(Execute := FALSE,Axis := AxisX);
			fbSlaveMoveVel(Execute := FALSE,Axis := AxisY);
			fbCamTableSelect(Master := AxisX,Slave := AxisY,CamTable := CamTable,Execute := FALSE);
			fbCamIn(Execute := FALSE,Master := AxisX,Slave := AxisY);
			fbCamOut(Slave := AxisY,Execute := FALSE);	
			fbMasterHalt(Axis := AxisX,Execute := FALSE);
			fbSlaveHalt(Axis := AxisY,Execute := FALSE);
			fbResetAxis(bExec := FALSE);
			fbSetActPos1(Axis := AxisX,Execute := FALSE,Mode := FALSE,Position := 0);
			fbSetActPos2(Axis := AxisY,Execute := FALSE,Mode := FALSE,Position := 0);
			fbResetAxis(bExec := FALSE);
			nState := 3;
		END_IF
		//设置主从轴的实际位置
		fbSetActPos1(Axis := AxisX,Execute := bSetMasterActPos,Mode := FALSE,Position := setMasterPos);
		fbSetActPos2(Axis := AxisY,Execute := bSetSlaveActPos,Mode := FALSE,Position := setSlavePos);

		//控制主从轴以一定的速度运动
		fbMasterMoveVel(Execute := bMasterRun,Axis := AxisX,Velocity := masterMotorVelTemp,Acceleration := masterMotorAccTemp,Deceleration := masterMotorAccTemp,Direction := MC_DIRECTION.positive);
		fbSlaveMoveVel(Execute := bSlaveRun,Axis := AxisY,Velocity := slaveMotorVelTemp,Acceleration := slaveMotorAccTemp,Deceleration := slaveMotorAccTemp,Direction := MC_DIRECTION.positive);
		
		//凸轮耦合
		fbCamTableSelect(Master := AxisX,Slave := AxisY,CamTable := CamTable,Execute := bGear,Periodic := bPeriodic,MasterAbsolute := bMasterAbs,SlaveAbsolute := bSlaveAbs);
		fbCamIn(Execute := fbCamTableSelect.Done,Master := AxisX,Slave := AxisY ,MasterOffset := masterOff,SlaveOffset := slaveOff,MasterScaling := masterSca,SlaveScaling := slaveSca,StartMode := startMode,CamTableID := fbCamTableSelect.CamTableID);
		fbCamOut(Slave := AxisY,Execute := bGearOut);	
		
		//轴停止
		fbMasterHalt(Axis := AxisX,Execute := bMasterStop,Deceleration := masterMotorAccTemp);
		fbSlaveHalt(Axis := AxisY,Execute := bSlaveStop,Deceleration := slaveMotorAccTemp);
		
	3:(* 将轴复位 *)
		fbResetAxis(bExec := TRUE);
		IF fbResetAxis.Done THEN
			fbResetAxis(bExec := FALSE);
			nState := 1;
		END_IF
END_CASE
//将主从轴的状态信息显示在视图中（使用F_AxisStatusToString函数）
fbReadStatusMaster(Axis := AxisX, Enable := TRUE);
fbReadStatusSlave(Axis := AxisY, Enable := TRUE);

// 使用F_AxisStatusToString函数转换状态
masterStateStr := F_AxisStatusToString(fbReadStatus := fbReadStatusMaster);
slaveStateStr := F_AxisStatusToString(fbReadStatus := fbReadStatusSlave);
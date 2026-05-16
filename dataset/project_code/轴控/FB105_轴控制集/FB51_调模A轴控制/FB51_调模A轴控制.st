PROGRAM FB51_调模A轴控制
VAR
	FB_AxisMotionDiag_调模A轴: FB_轴通讯状态块;
	FB_AxisStop_调模A轴: FB_轴停止触发块;
	
	SMC_SetControllerMode0: SMC_SetControllerMode;
	SMC_SetTorque0: SMC_SetTorque;
	SMC_ChangeGearingRatio0: SMC_ChangeGearingRatio;	
    MC_SetPosition_0: SM3_Basic.MC_SetPosition;	
	SMC_Homing_0: SM3_Basic.SMC_Homing;
	
	fb_CommunicationOK: TON;

	R_TRIG回零: R_TRIG;
	R_TRIG初始化回零: R_TRIG;
	b调模A轴手动定位: BOOL;
END_VAR

(*轴通讯状态*)
b调模A轴通讯OK:=FB_AxisMotionDiag_调模A轴.EtherCATBusOK;

FB_AxisMotionDiag_调模A轴(Axis_bCommunication:= AxisLeftTiaoMo.bCommunication, 
                        Axis_wCommunicationState:= AxisLeftTiaoMo.wCommunicationState, 
                        EtherCATBusOK=> );
						
fb_CommunicationOK(IN:= b调模A轴通讯OK, PT:= T#3S, Q=> , ET=> );

(*轴使能操作*)
IF NOT HMI_b调模A轴断使能 AND fb_CommunicationOK.Q THEN
	FB_AxisControl_调模A轴.Enable:=TRUE;
	ELSE
	FB_AxisControl_调模A轴.Enable:=FALSE;	
END_IF

(*轴控点动*)
IF HMI_b调模A轴正向点动 AND b调模A轴使能OK AND NOT b调模A轴错误 AND b非急停手动模式 AND NOT b调模A轴反向点动 THEN
	b调模A轴正向点动:=TRUE;
	ELSE
	b调模A轴正向点动:=FALSE;	
END_IF
IF HMI_b调模A轴反向点动 AND b调模A轴使能OK AND NOT b调模A轴错误 AND b非急停手动模式 AND NOT b调模A轴正向点动 THEN
	b调模A轴反向点动:=TRUE;
	ELSE
	b调模A轴反向点动:=FALSE;	
END_IF

(*轴控寸动*)
IF b调模A轴正向寸动 AND b调模A轴使能OK AND NOT b调模A轴错误 AND NOT FB_AxisControl_调模A轴.InchBackward THEN
	FB_AxisControl_调模A轴.InchForward:=TRUE;
	ELSE
	FB_AxisControl_调模A轴.InchForward:=FALSE;	
END_IF
IF b调模A轴反向寸动 AND b调模A轴使能OK AND NOT b调模A轴错误 AND NOT FB_AxisControl_调模A轴.InchForward THEN
	FB_AxisControl_调模A轴.InchBackward:=TRUE;
	ELSE
	FB_AxisControl_调模A轴.InchBackward:=FALSE;	
END_IF

(*轴控回零*)
R_TRIG回零(CLK:= SMC_Homing_0.bDone, Q=> );
R_TRIG初始化回零(CLK:= b调模A轴回零触发, Q=> );
IF (HMI_b调模A轴单独回原 OR R_TRIG初始化回零.Q) AND b调模A轴使能OK AND NOT b调模A轴错误 AND b非急停手动模式 AND NOT SMC_Homing_0.bBusy THEN
	SMC_Homing_0.bExecute:=TRUE;
END_IF
IF R_TRIG回零.Q THEN
	b调模A轴回零完成:=TRUE;
	SMC_Homing_0.bExecute:=FALSE;
END_IF

(*轴控绝对运动*)
IF b调模A轴绝对运动触发 AND b调模A轴使能OK AND NOT b调模A轴错误 THEN
	FB_AxisControl_调模A轴.AbsExcute:=TRUE;
	ELSE
	FB_AxisControl_调模A轴.AbsExcute:=FALSE;	
END_IF

(*轴控相对运动*)
IF b调模A轴相对运动触发 AND b调模A轴使能OK AND NOT b调模A轴错误 THEN
	FB_AxisControl_调模A轴.RelExcute:=TRUE;
	ELSE
	FB_AxisControl_调模A轴.RelExcute:=FALSE;	
END_IF

(*轴控定位*)
IF HMI_b调模A轴去工作位 AND b调模A轴使能OK AND NOT b调模A轴错误 AND b非急停手动模式 AND NOT b调模A轴绝对模式Busy AND NOT b调模A轴手动定位 THEN
	r调模A轴绝对运动位置给定:=HMI_r调模A轴宽度位置;
	b调模A轴绝对运动触发:=TRUE;
	b调模A轴手动定位:=TRUE;
END_IF
IF b调模A轴手动定位 AND b调模A轴绝对运动触发 AND b调模A轴绝对运动完成 THEN
	b调模A轴绝对运动触发:=FALSE;
	b调模A轴手动定位:=FALSE;	  
END_IF
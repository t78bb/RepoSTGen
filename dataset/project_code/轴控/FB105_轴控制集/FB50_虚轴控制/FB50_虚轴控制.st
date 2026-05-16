PROGRAM FB50_虚轴控制
VAR
	FB_AxisMotionDiag_AxisVirtual: FB_轴通讯状态块;
	SMC_SetControllerMode0: SMC_SetControllerMode;
	SMC_SetTorque0: SMC_SetTorque;
	SMC_ChangeGearingRatio0: SMC_ChangeGearingRatio;	
    MC_SetPosition_0: SM3_Basic.MC_SetPosition;	
	MC_GearIn_0: SM3_Basic.MC_GearIn;
	MC_GearOut_0: SM3_Basic.MC_GearOut;
	FB_AxisStop_AxisVirtual: FB_轴停止触发块;	
	
	fb_CommunicationOK: TON;
END_VAR

(*轴通讯状态*)
bAxisVirtual_CommunicationOK:=FB_AxisMotionDiag_AxisVirtual.EtherCATBusOK;

FB_AxisMotionDiag_AxisVirtual(Axis_bCommunication:= AxisVirtual.bCommunication, 
                        Axis_wCommunicationState:= AxisVirtual.wCommunicationState, 
                        EtherCATBusOK=> );
						
fb_CommunicationOK(IN:= bAxisVirtual_CommunicationOK, PT:= T#3S, Q=> , ET=> );

(*轴使能操作*)
IF NOT HMI_bAxisVirtual_PowerOff AND fb_CommunicationOK.Q THEN
	FB_AxisControl_AxisVirtual.Enable:=TRUE;
	ELSE
	FB_AxisControl_AxisVirtual.Enable:=FALSE;
END_IF

(*轴控点动*)
IF HMI_bAxisVirtual_JogForward AND bAxisVirtual_EnableOK AND NOT bAxisVirtual_Error AND b非急停手动模式 AND NOT bAxisVirtual_JogBack THEN
	bAxisVirtual_JogFor:=TRUE;
	ELSE
	bAxisVirtual_JogFor:=FALSE;	
END_IF
IF HMI_bAxisVirtual_BackForward AND bAxisVirtual_EnableOK AND NOT bAxisVirtual_Error AND b非急停手动模式 AND NOT bAxisVirtual_JogFor THEN
	bAxisVirtual_JogBack:=TRUE;
	ELSE
	bAxisVirtual_JogBack:=FALSE;	
END_IF

(*轴控寸动*)
IF bAxisVirtual_InchForExcute AND bAxisVirtual_EnableOK AND NOT bAxisVirtual_Error AND NOT FB_AxisControl_AxisVirtual.InchBackward THEN
	FB_AxisControl_AxisVirtual.InchForward:=TRUE;
	ELSE
	FB_AxisControl_AxisVirtual.InchForward:=FALSE;	
END_IF
IF bAxisVirtual_InchBackExcute AND bAxisVirtual_EnableOK AND NOT bAxisVirtual_Error AND NOT FB_AxisControl_AxisVirtual.InchForward THEN
	FB_AxisControl_AxisVirtual.InchBackward:=TRUE;
	ELSE
	FB_AxisControl_AxisVirtual.InchBackward:=FALSE;	
END_IF

(*轴控绝对运动*)
IF bAxisVirtual_AbsExcute AND bAxisVirtual_EnableOK AND NOT bAxisVirtual_Error THEN
	FB_AxisControl_AxisVirtual.AbsExcute:=TRUE;
	ELSE
	FB_AxisControl_AxisVirtual.AbsExcute:=FALSE;	
END_IF

(*轴控相对运动*)
IF bAxisVirtual_RelExcute AND bAxisVirtual_EnableOK AND NOT bAxisVirtual_Error THEN
	FB_AxisControl_AxisVirtual.RelExcute:=TRUE;
	ELSE
	FB_AxisControl_AxisVirtual.RelExcute:=FALSE;	
END_IF
VAR_GLOBAL
	FB_AxisControl_AxisVirtual: FB_轴控块;

//轴触发类	
	bAxisVirtual_CommunicationOK: BOOL; 
	bAxisVirtual_JogFor: BOOL;
	bAxisVirtual_JogBack: BOOL;
	bAxisVirtual_InchForExcute: BOOL;
	bAxisVirtual_InchBackExcute: BOOL;	
	bAxisVirtual_StopExcute: BOOL;
	bAxisVirtual_ResetExcute: BOOL;	
	bAxisVirtual_AbsExcute: BOOL;
	bAxisVirtual_RelExcute: BOOL;
	bAxisVirtual_VelExcute: BOOL;
	bAxisVirtual_LimitEnable: BOOL;

//轴状态类	
	bAxisVirtual_EnableOK: BOOL; 
	bAxisVirtual_StopDone: BOOL; 
	bAxisVirtual_AbsDone: BOOL; 
	bAxisVirtual_RelDone: BOOL; 
	bAxisVirtual_VelBusy: BOOL;
	bAxisVirtual_InchBusy: BOOL;
	bAxisVirtual_JogBusy: BOOL;
	bAxisVirtual_AbsBusy: BOOL;
	bAxisVirtual_RelBusy: BOOL;
	bAxisVirtual_Error: BOOL;
	bAxisVirtual_Accing: BOOL;
	bAxisVirtual_Decing: BOOL;
    bAxisVirtual_Standstill: BOOL;

//数据给定类
	rAxisVirtual_JogVelSet: LREAL;
	rAxisVirtual_AbsVelSet: LREAL;
	rAxisVirtual_RelVelSet: LREAL;
	rAxisVirtual_VelVelSet: LREAL;
	rAxisVirtual_InchVelSet: LREAL;
	
	rAxisVirtual_AbsPositionSet: LREAL;		
	rAxisVirtual_RelPositionSet: LREAL;
	rAxisVirtual_InchPositionSet: LREAL;
		
//数据读取类	
    rAxisVirtual_Actposition: LREAL;
	rAxisVirtual_ActVel: LREAL;
	rAxisVirtual_ActTorque: LREAL;
	
//其它类
    bAxisVirtual_HomeExcute: BOOL; 
    bAxisVirtual_HomeBusy: BOOL; 
    bAxisVirtual_HomeDone: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_bAxisVirtual_PowerOff: BOOL;
	HMI_bAxisVirtual_JogForward: BOOL;
    HMI_bAxisVirtual_BackForward: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL
	HMI_rAxisVirtual_ActPos: REAL;
	HMI_rAxisVirtual_ActVel: REAL;
	HMI_rAxisVirtual_AutoVel: REAL;
	HMI_rAxisVirtual_ManualVel: REAL;
	
	HMI_rAxisVirtual_Lead: REAL;
	HMI_rAxisVirtual_RatioMember: REAL;
	HMI_rAxisVirtual_RatioDenominator: REAL;
	
	HMI_rAxisVirtual_HomeFastVel: REAL;
	HMI_rAxisVirtual_HomeSlowVel: REAL;
	HMI_rAxisVirtual_LimitPostive: REAL;
	HMI_rAxisVirtual_LimitNegative: REAL;
	
	HMI_rAxisVirtual_AbsPos1: REAL;
	HMI_rAxisVirtual_AbsPos2: REAL;
	HMI_rAxisVirtual_AbsPos3: REAL;
	
	HMI_rAxisVirtual_RelPos1: REAL;
	HMI_rAxisVirtual_RelPos2: REAL;
	HMI_rAxisVirtual_RelPos3: REAL;
END_VAR



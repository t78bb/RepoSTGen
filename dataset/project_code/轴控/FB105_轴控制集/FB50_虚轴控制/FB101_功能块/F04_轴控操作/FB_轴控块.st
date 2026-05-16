FUNCTION_BLOCK FB_轴控块
VAR_INPUT
	Enable: BOOL;
	
	JogFor: BOOL;
	JogBack: BOOL;		
	JogVelocity :LREAL;
	
	StopExcute: BOOL;
	ResetExcute: BOOL;
	
	AbsExcute: BOOL;	
	AbsPosition: LREAL;
	AbsVelocity: LREAL;
	AbsAcceleration: LREAL;
	AbsDeceleration: LREAL;
	
	RelExcute: BOOL;
	RelPosition: LREAL;
	RelVelocity: LREAL;
	RelAcceleration: LREAL;
	RelDeceleration: LREAL;
	
	VelExcute: BOOL;
	VelVelocity: LREAL;
	
    InchForward: BOOL;
	InchBackward: BOOL;	
	InchDistance: LREAL;
	InchVelocity: LREAL;
	InchAcceleration: LREAL;
	InchDeceleration: LREAL;
	
	SetPosExcute: BOOL;

	ReStartSlaveEx: BOOL;
END_VAR
VAR_OUTPUT
	EnableStatus: BOOL;
	StopDone: BOOL;
	AbsDone: BOOL;
	RelDone: BOOL;
	VelBusy: BOOL;	
	InchBusy: BOOL;
	JogBusy: BOOL;
	AbsBusy: BOOL;
	RelBusy: BOOL;
	AxisStandstill: BOOL;
	AxisError: BOOL;
	AxisAccing: BOOL;
	AxisDecing: BOOL;
	FBErrorOccured: BOOL;
	Homing: BOOL;
	Stopping: BOOL;	
	ErrorID: SMC_ERROR;
	
	SetPosDone: BOOL;	

	bOperational: BOOL;
	eComState: SM3_Basic.SMC_CommunicationState;
	wComState: WORD;
	
	ReStartSlaveDone: BOOL;
END_VAR
VAR
	MC_Power0: MC_Power;
	MC_Jog0: MC_Jog;
	MC_Stop0: MC_Stop;
	MC_Reset0: MC_Reset;
	MC_MoveAbsolute0: MC_MoveAbsolute;
	MC_MoveRelative0: MC_MoveRelative;
	MC_MoveVelocity0: MC_MoveVelocity;
	MC_ReadStatus0: MC_ReadStatus;
	SMC_Inch0: SMC_Inch;
	MC_SetPosition0: MC_SetPosition;
	SMC_CheckAxisCommunication0: SMC_CheckAxisCommunication;
	SMC3_ReinitDrive0: SMC3_ReinitDrive;
END_VAR

VAR_IN_OUT
	AxisName: SM3_BASIC.AXIS_REF_SM3;
END_VAR

MC_Power0(
	Axis:= AxisName, 
	Enable:= TRUE, 
	bRegulatorOn:= Enable, 
	bDriveStart:= TRUE, 
	Status=> EnableStatus, 
	bRegulatorRealState=> , 
	bDriveStartRealState=> , 
	Busy=> , 
	Error=> , 
	ErrorID=> );
	
MC_Jog0(
	Axis:= AxisName, 
	JogForward:= JogFor, 
	JogBackward:= JogBack, 
	Velocity:= JogVelocity,  
	Acceleration:= JogVelocity*10000, 
	Deceleration:= JogVelocity*10000, 
	Jerk:= , 
	Busy=> JogBusy, 
	CommandAborted=> , 
	Error=> , 
	ErrorId=> );
	
MC_Stop0(
	Axis:= AxisName, 
	Execute:= StopExcute, 
	Deceleration:= 100000000, 
	Jerk:= , 
	Done=> StopDone, 
	Busy=> , 
	Error=> , 
	ErrorID=> );
	
MC_Reset0(
	Axis:= AxisName, 
	Execute:= ResetExcute, 
	Done=> , 
	Busy=> , 
	Error=> , 
	ErrorID=> );
	
	
MC_SetPosition0(
	Axis:= AxisName, 
	Execute:= SetPosExcute, 
	Position:= 0, 
	Mode:= 0, 
	Done=> SetPosDone, 
	Busy=> , 
	Error=> , 
	ErrorID=> );
	
MC_MoveAbsolute0(
	Axis:= AxisName, 
	Execute:= AbsExcute, 
	Position:= AbsPosition, 
	Velocity:= AbsVelocity, 
	Acceleration:= AbsAcceleration, 
	Deceleration:= AbsDeceleration, 
	Jerk:= , 
	Direction:= , 
	Done=> AbsDone, 
	Busy=> AbsBusy, 
	CommandAborted=> , 
	Error=> , 
	ErrorID=> );
	
MC_MoveRelative0(
	Axis:= AxisName, 
	Execute:= RelExcute, 
	Distance:= RelPosition, 
	Velocity:= RelVelocity, 
	Acceleration:= RelAcceleration, 
	Deceleration:= RelDeceleration, 
	Jerk:= , 
	Done=> RelDone, 
	Busy=> RelBusy, 
	CommandAborted=> , 
	Error=> , 
	ErrorID=> );
	
MC_MoveVelocity0(
	Axis:= AxisName, 
	Execute:= VelExcute, 
	Velocity:= VelVelocity, 
	Acceleration:= VelVelocity*10000, 
	Deceleration:= VelVelocity*10000, 
	Jerk:= , 
	Direction:= , 
	InVelocity=> , 
	Busy=> VelBusy, 
	CommandAborted=> , 
	Error=> , 
	ErrorID=> );	
	
MC_ReadStatus0(
	Axis:= AxisName, 
	Enable:= TRUE, 
	Valid=> , 
	Busy=> , 
	Error=> , 
	ErrorID=> ErrorID, 
	Disabled=> , 
	Errorstop=> AxisError, 
	Stopping=> Stopping, 
	StandStill=> AxisStandstill, 
	DiscreteMotion=> , 
	ContinuousMotion=> , 
	SynchronizedMotion=> , 
	Homing=> Homing, 
	ConstantVelocity=> , 
	Accelerating=> AxisAccing, 
	Decelerating=> AxisDecing, 
	FBErrorOccured=> FBErrorOccured);
	
SMC_Inch0(
	Axis:= AxisName, 
	InchForward:= InchForward, 
	InchBackward:= InchBackward, 
	Distance:= InchDistance, 
	Velocity:= InchVelocity, 
	Acceleration:= InchAcceleration, 
	Deceleration:= InchDeceleration, 
	Jerk:= , 
	Busy=> InchBusy, 
	CommandAborted=> , 
	Error=> , 
	ErrorId=> );
	
SMC_CheckAxisCommunication0(
	Axis:= AxisName, 
	bEnable:= TRUE, 
	bValid=> , 
	bError=> , 
	eErrorID=> , 
	bOperational=> bOperational, 
	eComState=> eComState, 
	wComState=> wComState);	
	
SMC3_ReinitDrive0(
	Axis:= AxisName, 
	bExecute:= ReStartSlaveEx, 
	bVirtual:= , 
	bDone=> ReStartSlaveDone, 
	bBusy=> , 
	bError=> , 
	nErrorID=> );
	
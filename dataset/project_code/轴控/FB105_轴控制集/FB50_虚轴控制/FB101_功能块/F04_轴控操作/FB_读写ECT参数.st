FUNCTION_BLOCK FB_读写ECT参数
VAR_INPUT
      Excute: BOOL;
      rWritePara1: REAL;
      rWritePara2: REAL;
      rWritePara3: REAL;
	  
      SlaveAddr: UINT;
	  
      SubIndexPara1: USINT;
      IndexPara1: UINT;
      SubIndexPara2: USINT;
      IndexPara2: UINT;
      SubIndexPara3: USINT;
      IndexPara3: UINT;
	  
      SubIndexVel: USINT;
      IndexVel: UINT;
      SubIndexTou: USINT;
      IndexTou: UINT;
END_VAR
VAR_OUTPUT
      rReadPara1: REAL;
      rReadPara2: REAL;
      rReadPara3: REAL;
      rActVel:    REAL;
      rActTouque: REAL;
END_VAR
VAR	  
	BLINK0: BLINK;
	
	SMC3_ETC_ReadParameter_CoE_Para1: SMC3_ETC_ReadParameter_CoE;
	SMC3_ETC_ReadParameter_CoE_Para2: SMC3_ETC_ReadParameter_CoE;
	SMC3_ETC_ReadParameter_CoE_Para3: SMC3_ETC_ReadParameter_CoE;
	SMC3_ETC_ReadParameter_CoE_Vel:   SMC3_ETC_ReadParameter_CoE;
	SMC3_ETC_ReadParameter_CoE_Tou:   SMC3_ETC_ReadParameter_CoE;
	
	SMC3_ETC_WriteParameter_CoE_Para1: SMC3_ETC_WriteParameter_CoE;
	SMC3_ETC_WriteParameter_CoE_Para2: SMC3_ETC_WriteParameter_CoE;
	SMC3_ETC_WriteParameter_CoE_Para3: SMC3_ETC_WriteParameter_CoE;
	SMC3_ETC_WriteParameter_CoE_Vel:   SMC3_ETC_WriteParameter_CoE;
	SMC3_ETC_WriteParameter_CoE_Tou:   SMC3_ETC_WriteParameter_CoE;
	
    ReadPara1			      : DWORD;        
	ReadPara2		          : DWORD;            
	ReadPara3			      : DWORD;          
	WritePara1			      : DWORD;         
	WritePara2		          : DWORD;             
	WritePara3			      : DWORD;       
	
	ReadActVel			      : INT;	  
	ReadActTouque		      : INT;	  
	
END_VAR

VAR_IN_OUT
	AxisName: SM3_Drive_ETC.AXIS_REF_ETC_SM3;
END_VAR

BLINK0(ENABLE:= Excute, TIMELOW:= T#500MS, TIMEHIGH:= T#500MS, OUT=> );

IF rReadPara1<>rWritePara1 AND Excute THEN
	SMC3_ETC_WriteParameter_CoE_Para1.xExecute:=TRUE;
	ELSE
	SMC3_ETC_WriteParameter_CoE_Para1.xExecute:=FALSE;	
END_IF
IF rReadPara2<>rWritePara2 AND Excute THEN
	SMC3_ETC_WriteParameter_CoE_Para2.xExecute:=TRUE;
	ELSE
	SMC3_ETC_WriteParameter_CoE_Para2.xExecute:=FALSE;	
END_IF
IF rReadPara3<>rWritePara3 AND Excute THEN
	SMC3_ETC_WriteParameter_CoE_Para3.xExecute:=TRUE;
	ELSE
	SMC3_ETC_WriteParameter_CoE_Para3.xExecute:=FALSE;	
END_IF

rReadPara1:=DWORD_TO_REAL(ReadPara1);
rReadPara2:=DWORD_TO_REAL(ReadPara2);
rReadPara3:=DWORD_TO_REAL(ReadPara3);
rActVel:=DWORD_TO_REAL(ReadActVel);
rActTouque:=DWORD_TO_REAL(ReadActTouque);

WritePara1:=REAL_TO_DWORD(rWritePara1);
WritePara2:=REAL_TO_DWORD(rWritePara2);
WritePara3:=REAL_TO_DWORD(rWritePara3);

(*读参数*)
SMC3_ETC_ReadParameter_CoE_Para1(
	xExecute:= BLINK0.OUT, 
	xAbort:= , 
	uiIndex:= IndexPara1, 
	usiSubIndex:= SubIndexPara1, 
	Axis:= AxisName, 
	xDone=> , 
	xBusy=> , 
	xError=> , 
	usiDataLength=> , 
	dwValue=> ADR(ReadPara1), 
	dwErrorCode=> , 
	eError=> );

SMC3_ETC_ReadParameter_CoE_Para2(
	xExecute:= BLINK0.OUT, 
	xAbort:= , 
	uiIndex:= IndexPara2, 
	usiSubIndex:= SubIndexPara2, 
	Axis:= AxisName, 
	xDone=> , 
	xBusy=> , 
	xError=> , 
	usiDataLength=> , 
	dwValue=> ADR(ReadPara2), 
	dwErrorCode=> , 
	eError=> );
	
SMC3_ETC_ReadParameter_CoE_Para3(
	xExecute:= BLINK0.OUT, 
	xAbort:= , 
	uiIndex:= IndexPara3, 
	usiSubIndex:= SubIndexPara3, 
	Axis:= AxisName, 
	xDone=> , 
	xBusy=> , 
	xError=> , 
	usiDataLength=> , 
	dwValue=> ADR(ReadPara3), 
	dwErrorCode=> , 
	eError=> );	

SMC3_ETC_ReadParameter_CoE_Vel(
	xExecute:= BLINK0.OUT, 
	xAbort:= , 
	uiIndex:= IndexVel, 
	usiSubIndex:= SubIndexVel, 
	Axis:= AxisName, 
	xDone=> , 
	xBusy=> , 
	xError=> , 
	usiDataLength=> , 
	dwValue=> ADR(ReadActVel), 
	dwErrorCode=> , 
	eError=> );		
	
SMC3_ETC_ReadParameter_CoE_Tou(
	xExecute:= BLINK0.OUT, 
	xAbort:= , 
	uiIndex:= IndexTou, 
	usiSubIndex:= SubIndexTou, 
	Axis:= AxisName, 
	xDone=> , 
	xBusy=> , 
	xError=> , 
	usiDataLength=> , 
	dwValue=> ADR(ReadActTouque), 
	dwErrorCode=> , 
	eError=> );		
	
	
	
(*写参数*)
SMC3_ETC_WriteParameter_CoE_Para1(
	xExecute:= , 
	xAbort:= , 
	uiIndex:= IndexPara1, 
	usiSubIndex:= SubIndexPara1, 
	usiDataLength:= DWORD_TO_USINT(SIZEOF(WritePara1)), 
	dwValue:= ADR(WritePara1), 
	Axis:= AxisName, 
	xDone=> , 
	xBusy=> , 
	xError=> , 
	dwErrorCode=> , 
	eError=> );
	
SMC3_ETC_WriteParameter_CoE_Para2(
	xExecute:= , 
	xAbort:= , 
	uiIndex:= IndexPara2, 
	usiSubIndex:= SubIndexPara2, 
	usiDataLength:= DWORD_TO_USINT(SIZEOF(WritePara2)), 
	dwValue:= ADR(WritePara2), 
	Axis:= AxisName, 
	xDone=> , 
	xBusy=> , 
	xError=> , 
	dwErrorCode=> , 
	eError=> );

SMC3_ETC_WriteParameter_CoE_Para3(
	xExecute:= , 
	xAbort:= , 
	uiIndex:= IndexPara3, 
	usiSubIndex:= SubIndexPara3, 
	usiDataLength:= DWORD_TO_USINT(SIZEOF(WritePara3)), 
	dwValue:= ADR(WritePara3), 
	Axis:= AxisName, 
	xDone=> , 
	xBusy=> , 
	xError=> , 
	dwErrorCode=> , 
	eError=> );


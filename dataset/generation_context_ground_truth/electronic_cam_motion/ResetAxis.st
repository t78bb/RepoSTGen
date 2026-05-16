VAR
	fbReset1	:	MC_Reset;
	fbReset2	:	MC_Reset;
	
	fbReadAxisError1	:	MC_ReadAxisError;
	fbReadAxisError2	:	MC_ReadAxisError;
	
	fbReadStatus1	:	MC_ReadStatus;
	fbReadStatus2	:	MC_ReadStatus;
	
	fbExecTrig	:	R_TRIG;
	nState 	:	BYTE;
	
	bErrorX	:	BOOL;
	bErrorY	:	BOOL;
	
END_VAR

VAR_OUTPUT 
	Done	:	BOOL;
END_VAR

fbExecTrig(CLK := bExec);

CASE nState OF 
	0:
		IF fbExecTrig.Q THEN
			nState := 1;
			Done := FALSE;
		END_IF
	1:
		fbReadAxisError1(Axis := AxisX ,Enable := TRUE);
		fbReadAxisError2(Axis := AxisY ,Enable := TRUE);
		
		fbReadStatus1(Axis := AxisX ,Enable := TRUE);
		fbReadStatus2(Axis := AxisY ,Enable := TRUE);
		
		IF fbReadAxisError1.Valid AND fbReadAxisError2.Valid AND fbReadStatus1.Valid AND fbReadStatus2.Valid THEN
			IF fbReadAxisError1.AxisError OR fbReadStatus1.FBErrorOccured THEN
				bErrorX := TRUE;
			ELSE
				bErrorX := FALSE;
			END_IF
			IF fbReadAxisError2.AxisError OR fbReadStatus2.FBErrorOccured THEN
				bErrorY := TRUE;
			ELSE
				bErrorY := FALSE;
			END_IF
			fbReadAxisError1(Axis := AxisX ,Enable := FALSE);
			fbReadAxisError2(Axis := AxisY ,Enable := FALSE);
			
			fbReadStatus1(Axis := AxisX ,Enable := FALSE);
			fbReadStatus2(Axis := AxisY ,Enable := FALSE);
			
			fbReset1(Axis := AxisX,Execute := FALSE);
			fbReset2(Axis := AxisY,Execute := FALSE);
			nState := 2;
		END_IF
	2:
		fbReset1(Axis := AxisX,Execute := bErrorX);
		fbReset2(Axis := AxisY,Execute := bErrorY);
		
		fbReadAxisError1(Axis := AxisX ,Enable := TRUE);
		fbReadAxisError2(Axis := AxisY ,Enable := TRUE);
		
		fbReadStatus1(Axis := AxisX ,Enable := TRUE);
		fbReadStatus2(Axis := AxisY ,Enable := TRUE);
		
		IF fbReadAxisError1.Valid AND fbReadAxisError2.Valid AND fbReadStatus1.Valid AND fbReadStatus2.Valid THEN
			IF NOT fbReadAxisError1.AxisError AND NOT fbReadAxisError2.AxisError (* AND NOT fbReadStatus1.FBErrorOccured AND NOT fbReadStatus2.FBErrorOccured AND NOT fbReadStatus3.FBErrorOccured *)THEN
				nState := 0;
				Done := TRUE;
				
				fbReadAxisError1(Axis := AxisX ,Enable := FALSE);
				fbReadAxisError2(Axis := AxisY ,Enable := FALSE);
				
				fbReset1(Axis := AxisX,Execute := FALSE);
				fbReset2(Axis := AxisY,Execute := FALSE);
				
				fbReadStatus1(Axis := AxisX ,Enable := FALSE);
				fbReadStatus2(Axis := AxisY ,Enable := FALSE);
			END_IF
		END_IF
END_CASE
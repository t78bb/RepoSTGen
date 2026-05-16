PROGRAM AUTO_CNC
VAR_INPUT
	bHome: BOOL;
	bCNC_Run: BOOL;
	bCNC_Stop: BOOL;
	bCNC_Reset: BOOL;
END_VAR
VAR
	bOpen: BOOL;
	set:BOOL;
	bServo_Enable: BOOL;
	bServo_Ready: BOOL;
	bError: BOOL;
	bHomeOK: BOOL;
	bAxisXHomeOK: BOOL;
	bAxisYHomeOK: BOOL;
	bAxisZHomeOK: BOOL;
	bOverrideADD: BOOL;
	bOverrideDEC: BOOL;
	
	iState: INT;
	poqPath: POINTER TO SMC_Outqueue;

	agcwBufReadNCFile: ARRAY[0..99] OF SMC_GCODE_WORD;
	agcdBuffer: ARRAY[0..99] OF SMC_GCODEVIEWER_DATA;
	agiBufDecoder: ARRAY [0..1] OF ARRAY[0..99] OF SMC_GeoInfo;
	agcsViewer: ARRAY[0..15] OF STRING;
	
	FBbHome_R_TRIG: R_TRIG;
	FBbHome_DoneX_R_TRIG: R_TRIG;
	FBbHome_DoneY_R_TRIG: R_TRIG;
	FBbHome_DoneZ_R_TRIG: R_TRIG;
	FBbCNC_Run_R_TRIG: R_TRIG;
	FBbCNC_Stop_R_TRIG: R_TRIG;
	FBbCNC_Reset_R_TRIG: R_TRIG;
	FBbOverrideADD_R_TRIG: R_TRIG;
	FBbOverrideDEC_R_TRIG: R_TRIG;
	
	(* 使用重构后的三轴控制功能块 *)
	fbTripleAxisPower	:	FB_TripleAxisPower;		//三轴电源控制
	fbTripleAxisStop	:	FB_TripleAxisStop;		//三轴停止控制
	fbTripleAxisReset	:	FB_TripleAxisReset;		//三轴复位控制
	fbTripleAxisHoming	:	FB_TripleAxisHoming;	//三轴回零控制
	
	(* 保留单独的Halt和Stop功能块（如需要） *)
	fbMC_AXISX_HALT: MC_HALT;
	fbMC_AXISY_HALT: MC_HALT;
	fbMC_AXISZ_HALT: MC_HALT;
	fbMC_AXISX_STOP: MC_STOP;
	fbMC_AXISY_STOP: MC_STOP;
	fbMC_AXISZ_STOP: MC_STOP;
	fbSMC_AXISX_HOMING: SMC_HOMING;
	fbSMC_AXISY_HOMING: SMC_HOMING;
	fbSMC_AXISZ_HOMING: SMC_HOMING;
	fbSMC_AXISX_READFBERROR: SMC_READFBERROR;
	fbSMC_AXISY_READFBERROR: SMC_READFBERROR;
	fbSMC_AXISZ_READFBERROR: SMC_READFBERROR;
	
	fbSMC_ReadNCFile: SMC_ReadNCFile;
	fbSMC_NCDecoder: SMC_NCDecoder;
	fbSMC_SmoothPath: SMC_SMOOTHPATH;
	fbSMC_CheckVelocities: SMC_CheckVelocities;
	fbSMC_Interpolator: SMC_Interpolator;
	fbSMC_ControlAxisXByPos: SMC_ControlAxisByPos;
	fbSMC_ControlAxisYByPos: SMC_ControlAxisByPos;
	fbSMC_ControlAxisZByPos: SMC_ControlAxisByPos;
	fbSMC_TRAFO_Gantry3: SMC_TRAFO_Gantry3;
	fbSMC_TRAFOF_Gantry3: SMC_TRAFOF_Gantry3;
	fbSMC_TRAFOF_Gantry3D: SMC_TRAFOF_Gantry3D;
	fbSMC_GCODEVIEWER: SMC_GCODEVIEWER;
END_VAR

set:=TRUE;

// 使用FB_TripleAxisPower进行三轴伺服使能
fbTripleAxisPower(
	AxisX := AXIS_X,
	AxisY := AXIS_Y,
	AxisZ := AXIS_Z,
	bServoEnable := bServo_Enable
);

// 更新错误状态
IF NOT bError THEN
	IF fbTripleAxisPower.bError THEN
		bError := TRUE;
		sSystem_Error := fbTripleAxisPower.sErrorString;
	END_IF
END_IF	


//插补运动	
FBbHome_R_TRIG(CLK:=bHome);	
FBbCNC_Run_R_TRIG(CLK:=bCNC_Run);
FBbCNC_Stop_R_TRIG(CLK:=bCNC_Stop);
//FBbCNC_Reset_R_TRIG(CLK:=bCNC_Reset);

// 使用功能块的Ready状态
bServo_Ready := fbTripleAxisPower.bReady;
IF bServo_Ready THEN

	CASE iState OF
	
	0:	// idle
		INIT();
		IF NOT bHomeOK THEN
			IF FBbHome_R_TRIG.Q THEN
				iState:=5;
			END_IF
		ELSE
			IF FBbCNC_Run_R_TRIG.Q THEN
				iState:=10;
			END_IF
		END_IF
	
	5://回零
	GoHome();
	IF bHomeOK THEN
		iState:=0;
	END_IF
	
	10:	// start reading and processing 
		//读G码文档
		fbSMC_ReadNCFile(
			bExecute:=TRUE , 
			sFileName:=sFilename , 
			pvl:= , 
			pBuffer:=ADR(agcwBufReadNCFile) , 
			dwBufferSize:=SIZEOF(agcwBufReadNCFile) , 
			fDefaultVel:= , 
			fDefaultAccel:= , 
			fDefaultDecel:= , 
			bDone=> , 
			bBusy=> , 
			bError=> , 
			ErrorID=> , 
			bExecuteDecoder=>, 
			ncprog=> );
		IF NOT bError THEN
			IF fbSMC_ReadNCFile.bError THEN
				bError:=TRUE;
				SMC_ERRORSTRING(ErrorID:=fbSMC_ReadNCFile.ErrorID,Language:=english,SMC_ErrorString=>sSystem_Error);
			END_IF
		END_IF
		//G码解析
		fbSMC_NCDecoder(
			bExecute:=fbSMC_ReadNCFile.bExecuteDecoder , 
			bAppend:= , 
			bStepSuppress:= , 
			piStartPosition:= , 
			nSizeOutQueue:=SIZEOF(agiBufDecoder[0]) , 
			pbyBufferOutQueue:=ADR(agiBufDecoder[0]) , 
			ncprog:=fbSMC_ReadNCFile.ncprog , 
			bDone=> , 
			bBusy=> , 
			bError=> , 
			wErrorID=> , 
			poqDataOut=> , 
			iStatus=> , 
			iLineNumberDecoded=> , 
			GCodeText=> );
		IF NOT bError THEN
			IF fbSMC_NCDecoder.bError THEN
				bError:=TRUE;
				SMC_ERRORSTRING(ErrorID:=fbSMC_NCDecoder.wErrorID,Language:=english,SMC_ErrorString=>sSystem_Error);
			END_IF
		END_IF
		//轨迹平滑处理	
		fbSMC_SmoothPath(
			bExecute:=fbSMC_ReadNCFile.bExecuteDecoder,
			poqDataIn:=fbSMC_NCDecoder.poqDataOut,
			nSizeOutQueue:=SIZEOF(agiBufDecoder[1]) , 
			pbyBufferOutQueue:=ADR(agiBufDecoder[1]) , 
			bSymmetricalDistances:=FALSE);
		IF NOT bError THEN
			IF fbSMC_SmoothPath.bError THEN
				bError:=TRUE;
				SMC_ERRORSTRING(ErrorID:=fbSMC_SmoothPath.wErrorID,Language:=english,SMC_ErrorString=>sSystem_Error);
			END_IF
		END_IF
		//轨迹速度处理
		fbSMC_CheckVelocities(
			bExecute:=fbSMC_ReadNCFile.bExecuteDecoder ,
			poqDataIn:=fbSMC_SmoothPath.poqDataOut , 
			dAngleTol:= 1, 
			bBusy=> , 
			bError=> , 
			wErrorID=> , 
			poqDataOut=>poqPath );
		IF NOT bError THEN
			IF fbSMC_CheckVelocities.bError THEN
				bError:=TRUE;
				SMC_ERRORSTRING(ErrorID:=fbSMC_CheckVelocities.wErrorID,Language:=english,SMC_ErrorString=>sSystem_Error);
			END_IF
		END_IF
		//插补运动
		fbSMC_Interpolator(
			bExecute:=fbSMC_ReadNCFile.bExecuteDecoder,
			dOverride:=(fOverride/100),
			poqDataIn:=poqPath,
			dwIpoTime:=dwIpoCycTime,
			bEmergency_Stop:=fbSMC_ControlAxisXByPos.bStopIpo OR fbSMC_ControlAxisYByPos.bStopIpo OR fbSMC_ControlAxisZByPos.bStopIpo);
		IF NOT bError THEN
			IF fbSMC_Interpolator.bError THEN
				bError:=TRUE;
				SMC_ERRORSTRING(ErrorID:=fbSMC_Interpolator.wErrorID,Language:=english,SMC_ErrorString=>sSystem_Error);
			END_IF
		END_IF		

		//坐标系偏移
		fbSMC_TRAFO_Gantry3(
			dOffsetX:=fAxisX_Offset,
			dOffsetY:=fAxisY_Offset,
			dOffsetz:=fAxisZ_Offset,
			pi:=fbSMC_Interpolator.piSetPosition);
			
		//轴运动控制
		fbSMC_ControlAxisXByPos(
			bEnable:=fbSMC_Interpolator.bWorking,
			iStatus:=fbSMC_Interpolator.iStatus,
			fSetPosition:=fbSMC_TRAFO_Gantry3.dx,
			fGapVelocity:=AXIS_X.fSWMaxVelocity,
			fGapAcceleration:=AXIS_X.fSWMaxAcceleration,
			fGapDeceleration:=AXIS_X.fSWMaxDeceleration,
			Axis:=AXIS_X);
		IF NOT bError THEN
			IF fbSMC_ControlAxisXByPos.bError THEN
				bError:=TRUE;
				SMC_ERRORSTRING(ErrorID:=fbSMC_ControlAxisXByPos.iErrorID,Language:=english,SMC_ErrorString=>sSystem_Error);
			END_IF
		END_IF	
			
		fbSMC_ControlAxisYByPos(
			bEnable:=fbSMC_Interpolator.bWorking,
			iStatus:=fbSMC_Interpolator.iStatus,
			fSetPosition:=fbSMC_TRAFO_Gantry3.dy,
			fGapVelocity:=AXIS_Y.fSWMaxVelocity,
			fGapAcceleration:=AXIS_Y.fSWMaxAcceleration,
			fGapDeceleration:=AXIS_Y.fSWMaxDeceleration,
			Axis:=AXIS_Y);
		IF NOT bError THEN
			IF fbSMC_ControlAxisYByPos.bError THEN
				bError:=TRUE;
				SMC_ERRORSTRING(ErrorID:=fbSMC_ControlAxisYByPos.iErrorID,Language:=english,SMC_ErrorString=>sSystem_Error);
			END_IF
		END_IF
			
		fbSMC_ControlAxisZByPos(
			bEnable:=fbSMC_Interpolator.bWorking,
			iStatus:=fbSMC_Interpolator.iStatus,
			fSetPosition:=fbSMC_TRAFO_Gantry3.dz,
			fGapVelocity:=AXIS_Z.fSWMaxVelocity,
			fGapAcceleration:=AXIS_Z.fSWMaxAcceleration,
			fGapDeceleration:=AXIS_Z.fSWMaxDeceleration,
			Axis:=AXIS_Z);
		IF NOT bError THEN
			IF fbSMC_ControlAxisZByPos.bError THEN
				bError:=TRUE;
				SMC_ERRORSTRING(ErrorID:=fbSMC_ControlAxisZByPos.iErrorID,Language:=english,SMC_ErrorString=>sSystem_Error);
			END_IF
		END_IF
		
		IF fbSMC_Interpolator.bDone THEN
			iState:=20;
		END_IF
		AXIS_SIM();
		Act_Gline:=AUTO_CNC.fbSMC_Interpolator.iObjNo;
		
		20:
		INIT();
		iState:=10;
		
	END_CASE
	
ELSE
	INIT();
	bHomeOK:=FALSE;
	iState:=0;
END_IF

// 使用FB_TripleAxisStop进行三轴停止
fbTripleAxisStop(
	AxisX := AXIS_X,
	AxisY := AXIS_Y,
	AxisZ := AXIS_Z,
	bExecute := FBbCNC_Stop_R_TRIG.Q,
	rDeceleration := 100.0
);

// 错误检查
IF NOT bError THEN
	IF fbTripleAxisStop.bError THEN
		bError := TRUE;
		sSystem_Error := fbTripleAxisStop.sErrorString;
	END_IF
END_IF

// 停止完成后复位状态
IF fbTripleAxisStop.bDone THEN
	bHomeOK := FALSE;
	iState := 0;
END_IF

// 使用FB_TripleAxisReset进行三轴复位
fbTripleAxisReset(
	AxisX := AXIS_X,
	AxisY := AXIS_Y,
	AxisZ := AXIS_Z,
	bExecute := bCNC_Reset
);

// 错误检查
IF NOT bError THEN
	IF fbTripleAxisReset.bError THEN
		bError := TRUE;
		sSystem_Error := fbTripleAxisReset.sErrorString;
	END_IF
END_IF

// 复位完成后清除错误并复位状态
IF bCNC_Reset THEN
	bError := FALSE;
	iState := 0;
END_IF

// 默认状态：无错误
IF NOT bError THEN
	sSystem_Error := 'CNC_NO_ERROR';
END_IF
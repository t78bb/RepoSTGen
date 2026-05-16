PROGRAM PLC_PRG
VAR
	FB_BaseDetector: F_TRIG;
	FB_LidDetector: F_TRIG;
	FB_PartDetector: F_TRIG;
	FB_PnPMachine: PNP_MACHINE;
	FB_LidPickedNotification: R_TRIG;
	FB_LidPlacedNotification: R_TRIG;
	FB_BaseClamperRaised: F_TRIG;
	
	_BaseConveyorState: BOOL := TRUE;
	_LidConveyorState: BOOL := TRUE;
	_baseClamped: BOOL := FALSE;
	_lidClamped: BOOL := FALSE;
	_baseClampPosition: BOOL := FALSE;
	_moveBaseClamp: BOOL := FALSE;
	_partLeft: BOOL := FALSE;
	PartCounter: WORD := 0;
END_VAR

FB_BaseDetector(CLK := FIO.FIO_iBaseAtPlace);
FB_LidDetector(CLK := FIO.FIO_iLidAtPlace);
FB_PartDetector(CLK := FIO.FIO_iPartLeaving);
FB_PnPMachine(BaseClamped := _BaseClamped, LidClamped := _LidClamped);
FB_LidPickedNotification(CLK:= FB_PnPMachine.LidPicked);
FB_LidPlacedNotification(CLK:= FB_PnPMachine.LidPlaced);
FB_BaseClamperRaised(CLK:= FIO.FIO_iBasePosAtLimit);

IF FIO.FIO_iReset THEN
	_baseConveyorState:= TRUE;
	_lidConveyorState:= TRUE;
	_baseClamped := FALSE;
	_lidClamped := FALSE;
	_baseClampPosition := FALSE;
	_moveBaseClamp := FALSE;
	_partLeft := FALSE;
	PartCounter := 0;
	FB_PnPMachine.Reset := TRUE;
END_IF

FIO.FIO_oLidsConveyor := _lidConveyorState;
FIO.FIO_oBasesConveyor := _baseConveyorState;

FIO.FIO_oClampLid := _lidClamped;
FIO.FIO_oClampBase := _baseClamped;
FIO.FIO_oBasePosRaise := _moveBaseClamp;
FIO.FIO_oCounter := PartCounter;

_baseConveyorState := NOT _baseClamped;
_lidConveyorState := NOT _LidClamped;

IF FB_BaseDetector.Q THEN
	_BaseClamped := TRUE;
END_IF

IF FB_LidDetector.Q THEN
	_LidClamped := TRUE;
END_IF

IF FB_LidPickedNotification.Q THEN
	_LidClamped := FALSE;
END_IF

IF FB_LidPlacedNotification.Q THEN
	_BaseClamped := FALSE;
	_moveBaseClamp := TRUE;
END_IF

IF FB_BaseClamperRaised.Q THEN
	_baseClampPosition := TRUE;
END_IF

IF FB_PartDetector.Q THEN
	_partLeft := TRUE;
	PartCounter := PartCounter +1;
END_IF

IF _partLeft AND _baseClampPosition THEN
	_moveBaseClamp := FALSE;
	_partLeft := FALSE;
	_baseClampPosition:= FALSE;
END_IF
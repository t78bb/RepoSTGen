VAR
	FB_ItemDetect : R_TRIG;
	FB_MovingZ: F_TRIG;
	FB_MovingX : F_TRIG;
	
	_pickerMoved: BOOL := FALSE;
	_movePicker: BOOL := FALSE;
	_moveArm: BOOL := FALSE;
	_armMoved : BOOL := FALSE;
	_grabItem: BOOL := FALSE;
	_itemDetected: BOOL := FALSE;
	_gripperAtLid: BOOL := FALSE;
	_gripperAtBase: BOOL := FALSE;
END_VAR

FB_MovingZ(CLK := FIO.FIO_iMovingZ);
FB_MovingX(CLK:= FIO.FIO_iMovingX);
FB_ItemDetect(CLK := FIO.FIO_iItemDetected);

FIO.FIO_oMoveZ := _movePicker;
FIO.FIO_oGrab := _grabItem;
FIO.FIO_oMoveX := _moveArm;

IF Reset THEN
	_pickerMoved := FALSE;
	_movePicker := FALSE;
	_grabItem := FALSE;
	_moveArm := FALSE;
	_armMoved := FALSE;
	LidPicked := FALSE;
	LidPlaced := FALSE;
	_itemDetected := FALSE;
	_gripperAtLid := FALSE;
	_gripperAtBase := FALSE;
END_IF

IF FB_MovingZ.Q THEN
	_pickerMoved := NOT _pickerMoved;
END_IF

IF FB_MovingX.Q THEN
	_armMoved := NOT _armMoved;
END_IF

IF FB_ItemDetect.Q THEN
	_itemDetected:= TRUE;
END_IF

// Picker movement for Lid
IF (BaseClamped AND LidClamped) THEN
	_movePicker := TRUE;
END_IF

IF _grabItem THEN
	_movePicker := FALSE;
	LidPicked := TRUE;
	LidPlaced := FALSE;
END_IF

// Picker movement for Base
IF _armMoved AND _grabItem THEN
	_movePicker:= TRUE;
END_IF

IF _armMoved AND NOT _grabItem THEN
	_movePicker:= FALSE;
END_IF

// Gripper
_gripperAtLid := _pickerMoved AND NOT _armMoved;
_gripperAtBase := _pickerMoved AND _armMoved;

IF _gripperAtLid AND _itemDetected THEN
	_grabItem := TRUE;
END_IF

IF _gripperAtBase AND _grabItem THEN
	_grabItem := FALSE;
	_itemDetected := FALSE;
	LidPlaced := TRUE;
	LidPicked := FALSE;
END_IF

// arm movement
IF LidPicked AND NOT _pickerMoved THEN
	_moveArm := TRUE;
END_IF

IF LidPlaced AND NOT _pickerMoved THEN
	_moveArm := FALSE;
END_IF

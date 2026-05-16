// 使用FB_TripleAxisHoming进行三轴回零
fbTripleAxisHoming(
	bExecute := NOT bHomeOK,
	AxisX := AXIS_X,
	AxisY := AXIS_Y,
	AxisZ := AXIS_Z,
	bAxisXRefSwitch := bAxisXReferenceSwitch,
	bAxisYRefSwitch := bAxisYReferenceSwitch,
	bAxisZRefSwitch := bAxisZReferenceSwitch,
	fVelocitySlow := fHomeVelocitySlow,
	fVelocityFast := fHomeVelocityFast,
	fAcceleration := fHomeAcceleration,
	fDeceleration := fHomeDeceleration
);

// 更新回零状态
bHomeOK := fbTripleAxisHoming.bHomeOK;
bAxisXHomeOK := fbTripleAxisHoming.bAxisXHomeOK;
bAxisYHomeOK := fbTripleAxisHoming.bAxisYHomeOK;
bAxisZHomeOK := fbTripleAxisHoming.bAxisZHomeOK;

// 错误处理
IF NOT bError THEN
	IF fbTripleAxisHoming.bError THEN
		bError := TRUE;
		sSystem_Error := fbTripleAxisHoming.sErrorString;
	END_IF
END_IF
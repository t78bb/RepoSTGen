
// 根据轴状态返回对应的字符串描述
// 按优先级顺序检查状态

IF fbReadStatus.Errorstop THEN
	F_AxisStatusToString := 'Errorstop';
	RETURN;
END_IF

IF fbReadStatus.Disabled THEN
	F_AxisStatusToString := 'Disabled';
	RETURN;
END_IF

IF fbReadStatus.Homing THEN
	F_AxisStatusToString := 'Homing';
	RETURN;
END_IF

IF fbReadStatus.Stopping THEN
	F_AxisStatusToString := 'Stopping';
	RETURN;
END_IF

IF fbReadStatus.SynchronizedMotion THEN
	F_AxisStatusToString := 'SynchronizedMotion';
	RETURN;
END_IF

IF fbReadStatus.ContinuousMotion THEN
	F_AxisStatusToString := 'ContinuousMotion';
	RETURN;
END_IF

IF fbReadStatus.DiscreteMotion THEN
	F_AxisStatusToString := 'DiscreteMotion';
	RETURN;
END_IF

IF fbReadStatus.StandStill THEN
	F_AxisStatusToString := 'StandStill';
	RETURN;
END_IF

// 默认状态
F_AxisStatusToString := 'Unknown';


// 复位回零标志
bAxisXHomeOK := FALSE;
bAxisYHomeOK := FALSE;
bAxisZHomeOK := FALSE;
Act_Gline := 0;

// 使用INIT_CNC_System函数进行系统初始化
INIT_CNC_System(
	fbSMC_ReadNCFile := fbSMC_ReadNCFile,
	fbSMC_NCDecoder := fbSMC_NCDecoder,
	fbSMC_CheckVelocities := fbSMC_CheckVelocities,
	fbSMC_Interpolator := fbSMC_Interpolator,
	fbSMC_ControlAxisXByPos := fbSMC_ControlAxisXByPos,
	fbSMC_ControlAxisYByPos := fbSMC_ControlAxisYByPos,
	fbSMC_ControlAxisZByPos := fbSMC_ControlAxisZByPos,
	fbSMC_AXISX_HOMING := fbSMC_AXISX_HOMING,
	fbSMC_AXISY_HOMING := fbSMC_AXISY_HOMING,
	fbSMC_AXISZ_HOMING := fbSMC_AXISZ_HOMING,
	fbMC_AXISX_STOP := fbMC_AXISX_STOP,
	fbMC_AXISY_STOP := fbMC_AXISY_STOP,
	fbMC_AXISZ_STOP := fbMC_AXISZ_STOP,
	AxisX := AXIS_X,
	AxisY := AXIS_Y,
	AxisZ := AXIS_Z
);

//fbSMC_GCODEVIEWER(bEnable:=FALSE,GCodeText:=fbSMC_NCDecoder.GCodeText);
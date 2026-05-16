FUNCTION INIT_CNC_System : BOOL
VAR_IN_OUT
	fbSMC_ReadNCFile		:	SMC_ReadNCFile;
	fbSMC_NCDecoder			:	SMC_NCDecoder;
	fbSMC_CheckVelocities	:	SMC_CheckVelocities;
	fbSMC_Interpolator		:	SMC_Interpolator;
	fbSMC_ControlAxisXByPos	:	SMC_ControlAxisByPos;
	fbSMC_ControlAxisYByPos	:	SMC_ControlAxisByPos;
	fbSMC_ControlAxisZByPos	:	SMC_ControlAxisByPos;
	fbSMC_AXISX_HOMING		:	SMC_HOMING;
	fbSMC_AXISY_HOMING		:	SMC_HOMING;
	fbSMC_AXISZ_HOMING		:	SMC_HOMING;
	fbMC_AXISX_STOP			:	MC_STOP;
	fbMC_AXISY_STOP			:	MC_STOP;
	fbMC_AXISZ_STOP			:	MC_STOP;
END_VAR
VAR_INPUT
	AxisX					:	SM3_Basic.AXIS_REF_SM3
	AxisY					:	SM3_Basic.AXIS_REF_SM3
	AxisZ					:	SM3_Basic.AXIS_REF_SM3
END_VAR

// 复位回零标志
// 注意：这里不能直接修改VAR_INPUT的变量，需要在调用处理

// 复位G代码处理相关功能块
fbSMC_ReadNCFile(bExecute := FALSE);
fbSMC_NCDecoder(bExecute := FALSE, ncprog := fbSMC_ReadNCFile.ncprog);
fbSMC_CheckVelocities(bExecute := FALSE);
fbSMC_Interpolator(bExecute := FALSE);

// 复位轴控制功能块
fbSMC_ControlAxisXByPos(bEnable := FALSE, Axis := AxisX);
fbSMC_ControlAxisYByPos(bEnable := FALSE, Axis := AxisY);
fbSMC_ControlAxisZByPos(bEnable := FALSE, Axis := AxisZ);

// 复位回零功能块
fbSMC_AXISX_HOMING(bExecute := FALSE, Axis := AxisX);
fbSMC_AXISY_HOMING(bExecute := FALSE, Axis := AxisY);
fbSMC_AXISZ_HOMING(bExecute := FALSE, Axis := AxisZ);

// 复位停止功能块
fbMC_AXISX_STOP(Execute := FALSE, Deceleration := 100, Axis := AxisX);
fbMC_AXISY_STOP(Execute := FALSE, Deceleration := 100, Axis := AxisY);
fbMC_AXISZ_STOP(Execute := FALSE, Deceleration := 100, Axis := AxisZ);

// 返回TRUE表示初始化完成
INIT_CNC_System := TRUE;


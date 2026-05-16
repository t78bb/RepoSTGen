
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


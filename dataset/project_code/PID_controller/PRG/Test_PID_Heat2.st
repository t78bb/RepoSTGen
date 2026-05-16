PROGRAM Test_PID_Heat2
VAR
	PID_controller_0: PID_controller;
	HeatExchanger2_0: HeatExchanger2;
	SP: REAL := 300;
	Temp_out: REAL := 270;
END_VAR

PID_controller_0(
    SP := SP,                // 设定值：目标液位250
    PV := HeatExchanger2_0.Temp,              // 过程值：储罐当前液位（反馈）
    Kc := 50,                  // 比例增益2.0
    Ti := 5,                  // 积分时间15.0
    Td := 0,                  // 微分时间1.0
    SampleTime := T#250ms,  // 采样时间100ms
    LowerLimit := 0,  // 输出下限0
    UpperLimit := 6000,  // 输出上限150
    CO => ,                  // PID输出：控制储罐的输入流量
    CO_P => ,                      // 比例部分输出（未使用可留空）
    CO_I => ,                      // 积分部分输出（未使用可留空）
    CO_D =>                        // 微分部分输出（未使用可留空）
);

// 2. 调用储罐功能块
HeatExchanger2_0(
    Heat_In := PID_controller_0.CO,
    U := 100,   
    TC := 2500,
    Temp_In := 270,
    Temp_Out := Temp_Out;
    Sample_time := T#100ms,
    Temp =>            
);
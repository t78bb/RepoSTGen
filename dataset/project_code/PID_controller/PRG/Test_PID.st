PROGRAM Test_PID
VAR
	PID_0: PID_controller;
	RedBull: Tank;
	Process_out: REAL := 100;
	SetPoint: REAL := 250;
END_VAR

VAR CONSTANT
END_VAR

PID_0(
    SP := SetPoint,                // 设定值：目标液位250
    PV := RedBull.Level,              // 过程值：储罐当前液位（反馈）
    Kc := 2,                  // 比例增益2.0
    Ti := 15,                  // 积分时间15.0
    Td := 1,                  // 微分时间1.0
    SampleTime := T#100ms,  // 采样时间100ms
    LowerLimit := 0,  // 输出下限0
    UpperLimit := 150,  // 输出上限150
    CO => ,                  // PID输出：控制储罐的输入流量
    CO_P => ,                      // 比例部分输出（未使用可留空）
    CO_I => ,                      // 积分部分输出（未使用可留空）
    CO_D =>                        // 微分部分输出（未使用可留空）
);

// 2. 调用储罐功能块
RedBull(
    Process_In := PID_0.CO,          // 输入流量：PID的输出CO
    Process_Out := Process_out,    // 输出流量：100（外部定义）
    Sample_time := T#250ms,// 采样时间250ms
    Lower_limit := 0,// 液位下限0
    Upper_limit := 500,// 液位上限500
    Level =>             // 输出当前液位：反馈给PID的PV
);
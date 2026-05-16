FUNCTION_BLOCK FB_EdgeDetection
VAR_INPUT
    bExecute : BOOL; // FBD图的输入信号
END_VAR
VAR_OUTPUT
    Out_s    : BOOL; // 对应 FBD图中的 Out[s] (启动信号脉冲)
    Out_e    : BOOL; // 对应 FBD图中的 Out[e] (结束信号脉冲)
END_VAR
VAR
    // 必须声明 R_TRIG 和 F_TRIG 的实例来存储上一周期的状态
    RTrig_Inst : R_TRIG; 
    FTrig_Inst : F_TRIG;
END_VAR
// ...


// -----------------------------------------------------
// 1. 上升沿检测 (R_TRIG)
// -----------------------------------------------------
RTrig_Inst(
    CLK := bExecute,
    Q   => Out_s
);

// -----------------------------------------------------
// 2. 下降沿检测 (F_TRIG)
// -----------------------------------------------------
FTrig_Inst(
    CLK := bExecute,
    Q   => Out_e
);
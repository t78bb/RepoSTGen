PROGRAM A03_原点回归
VAR
    MC_SetPosition_0 : SM3_Basic.MC_SetPosition; (* 声明位置设置功能块 *)
END_VAR

VAR_INPUT
END_VAR

VAR_OUTPUT
END_VAR

VAR_IN_OUT
END_VAR

(* 调用MC_SetPosition功能块，实现轴位置设置 *)
MC_SetPosition_0(
    Axis := AxisVirtual,
    Execute := ,
    Position := 0,
    Mode := 0,
    Done => ,
    Busy => ,
    Error => ,
    ErrorID =>
);
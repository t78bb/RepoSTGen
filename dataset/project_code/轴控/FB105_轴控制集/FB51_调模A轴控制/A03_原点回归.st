PROGRAM A03_原点回归
VAR
    MC_SetPosition_0 : SM3_Basic.MC_SetPosition; (* 声明位置设置功能块 *)
    SMC_Homing_0 : SM3_Basic.SMC_Homing;
END_VAR

VAR_INPUT
END_VAR

VAR_OUTPUT
END_VAR

VAR_IN_OUT
END_VAR

(* 调用MC_SetPosition功能块，实现轴位置设置 *)
MC_SetPosition_0(
    Axis := AxisLeftTiaoMo,
    Execute := ,
    Position := 0,
    Mode := 0,
    Done => ,
    Busy => ,
    Error => ,
    ErrorID =>
);

SMC_Homing_0(
    Axis := AxisLeftTiaoMo,
    bExecute := ,
    fHomePosition := 0,
    fVelocitySlow := HMI_r调模A轴回零慢速,
    fVelocityFast := HMI_r调模A轴回零快速,
    fAcceleration := HMI_r调模A轴回零快速*10000,
    fDeceleration := HMI_r调模A轴回零快速*10000,
    fJerk := ,
    nDirection := -1,
    bReferenceSwitch := DI_调模A步进原点,
    fSignalDelay := ,
    nHomingMode := 1,
    bReturnToZero := ,
    bIndexOccured := ,
    fIndexPosition := ,
    bIgnoreHWLimit := ,
    bDone => ,
    bBusy => ,
    bCommandAborted => ,
    bError => ,
    nErrorID => ,
    bStartLatchingIndex => 
);

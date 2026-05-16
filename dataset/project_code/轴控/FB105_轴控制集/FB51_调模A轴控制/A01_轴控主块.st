PROGRAM A01_轴控主块
VAR
    FB_AxisControl_调模A轴 : FB_轴控块; (* 声明位置设置功能块 *)
    FB_AxisStop_调模A轴 : FB_轴停止触发块;
    SMC_ChangeGearingRatio0 : SMC_ChangeGearingRatio;
    SMC_SetControllerMode0 : SMC_SetControllerMode; 
    SMC_SetTorque0 : SMC_SetTorque;
    bDone_SetMode : BOOL;    
END_VAR

VAR_INPUT
END_VAR

VAR_OUTPUT
END_VAR

VAR_IN_OUT
END_VAR

FB_AxisControl_调模A轴(
    Enable := , // 使能轴（可根据实际逻辑控制）
    JogFor := b调模A轴正向点动,
    JogBack := b调模A轴反向点动,
    JogVelocity := r调模A轴点动速度给定,
    StopExcute := b调模A轴停止触发,
    ResetExcute := HMI_b复位,
    AbsExcute := , // 初始设为FALSE，需触发时置TRUE
    AbsPosition := r调模A轴绝对运动位置给定,
    AbsVelocity := r调模A轴绝对运动速度给定,
    // AbsAcceleration 等参数若有默认值或无需外部给定，可省略或按实际赋值
    AbsAcceleration := ,
    AbsDeceleration := ,
    RelExcute := ,
    RelPosition := r调模A轴相对运动位置给定,
    RelVelocity := r调模A轴相对运动速度给定,
    // RelAcceleration 等参数同理
    RelAcceleration := ,
    RelDeceleration := ,
    VelExcute := ,
    VelVelocity := r调模A轴速度模式速度给定,
    InchForward := ,
    InchBackward := ,
    InchDistance := r调模A轴寸动位置给定,
    InchVelocity := r调模A轴寸动速度给定,
    // InchAcceleration 等参数同理
    InchAcceleration := ,
    InchDeceleration := ,
    SetPosExcute := ,
    ReStartSlaveEx := ,
    AxisName := AxisLeftTiaoMo,

    // 输出映射
    EnableStatus => b调模A轴使能OK,
    StopDone => b调模A轴停止完成,
    AbsDone => b调模A轴绝对运动完成,
    RelDone => b调模A轴相对运动完成,
    VelBusy => b调模A轴速度模式Busy,
    InchBusy => b调模A轴寸动模式Busy,
    AxisStandsstill => b调模A轴停止中,
    AbsBusy => b调模A轴绝对模式Busy,
    RelBusy => b调模A轴相对模式Busy,
    AxisError => b调模A轴错误,
    AxisAccing => b调模A轴加速中,
    AxisDecing => b调模A轴减速中,
    FBErrorOccured => ,
    Homing => ,
    Stopping => ,
    ErrorID => ,
    SetPosDone => ,
    bOperational => ,
    eComState => ,
    wComState => ,
    JogBusy => b调模A轴点动模式Busy
    ReStartSlaveDone =>
    // 其他输出需按功能块定义补充映射
);

FB_AxisStop_调模A轴(
    StopExcute := b调模A轴停止触发
);

SMC_ClearFBError_Instance(
    EN := FBErrorOccurred,
    pDrive := ADR(AxisLeftTiaoMo),
    ENO => ,
    SMC_ClearFBError =>
);

SMC_ChangeGearingRatio0(
    Axis := AxisLeftTiaoMo,
    bExecute := ,
    dwRatioTechUnitsDenom := AxisLeftTiaoMo.dwRatioTechUnitsDenom,
    iRatioTechUnitsNum := REAL_TO_INT(HMI_r调模A轴导程),
    fPositionPeriod := fPositionPeriod,
    iMovementType := SMC_MOVEMENTTYPE.linear,
   
    bDone => ,
    bBusy => ,
    bError => ,
    nErrorID => 
);

AxisLeftTiaoMo_iRestNumerator := 0;

SMC_SetControllerMode0(
    Axis := AxisLeftTiaoMo,
    bExecute := ,
    nControllerMode := SMC_CONTROLLER_MODE.SMC_torque,
    bDone => bDone_SetMode,
    bBusy => ,
    bError => ,
    nErrorID => 
);

// 调用 SMC_SetTorque 功能块，设置扭矩
SMC_SetTorque0(
    Axis := AxisLeftTiaoMo,
    bEnable := bDone_SetMode,
    fTorque := ,
    bBusy => ,
    bError => ,
    nErrorID => 
);
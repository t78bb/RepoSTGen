PROGRAM A01_轴控主块
VAR
	FB_AxisControl_AxisVirtual : FB_轴控块;
	FB_AxisStop_AxisVirtual : FB_轴停止触发块;
	SMC_ChangeGearingRatio0 : SMC_ChangeGearingRatio;
END_VAR

VAR_INPUT
END_VAR

VAR_OUTPUT
END_VAR

VAR_IN_OUT
END_VAR


FB_AxisControl_AxisVirtual(
    (* =============== 输入参数 ( := ) =============== *)
    Enable             := ,                        (* 图中未连接，留空 *)
    JogFor             := bAxisVirtual_JogFor,
    JogBack            := bAxisVirtual_JogBack,
    JogVelocity        := rAxisVirtual_JogVelSet,   (* JogVelocity 连线到 rAxisVirtual_JogVelSet *)
    StopExecute        := bAxisVirtual_StopExcute,
    ResetExecute       := HMI_b复位,                (* ResetExecute 连线到 HMI_b复位 *)

    AbsExecute         := ,                        (* 图中未连接，留空 *)
    AbsPosition        := rAxisVirtual_AbsPositionSet,
    AbsVelocity        := rAxisVirtual_AbsVelSet,
    AbsAcceleration    := ,                        (* 图中未连接，留空 *)
    AbsDeceleration    := ,                        (* 图中未连接，留空 *)

    RelExecute         := ,                        (* 图中未连接，留空 *)
    RelPosition        := rAxisVirtual_RelPositionSet,
    RelVelocity        := rAxisVirtual_RelVelSet,
    RelAcceleration    := ,                        (* 图中未连接，留空 *)
    RelDeceleration    := ,                        (* 图中未连接，留空 *)

    VelExecute         := ,                        (* 图中未连接，留空 *)
    VelVelocity        := rAxisVirtual_VelVelSet,

    InchForward        := ,                        (* 图中未连接，留空 *)
    InchBackward       := ,                        (* 图中未连接，留空 *)
    InchDistance       := rAxisVirtual_InchPositionSet,
    InchVelocity       := rAxisVirtual_InchVelSet,
    InchAcceleration   := ,                        (* 图中未连接，留空 *)
    InchDeceleration   := ,                        (* 图中未连接，留空 *)

    SetPosExecute      := ,                        (* 图中未连接，留空 *)
    ReStartSlaveEx     := ,                        (* 图中未连接，留空 *)
    AxisName           := AxisVirtual,              (* AxisName 连线到 AxisVirtual *)


    (* =============== 输出参数 ( => ) =============== *)
    EnableStatus       => bAxisVirtual_EnableOK,
    StopDone           => bAxisVirtual_StopDone,
    AbsDone            => bAxisVirtual_AbsDone,
    RelDone            => bAxisVirtual_RelDone,
    VelBusy            => bAxisVirtual_VelBusy,
    InchBusy           => bAxisVirtual_InchBusy,
    AxisStandstill     => bAxisVirtual_Standstill,
    AbsBusy            => bAxisVirtual_AbsBusy,
    RelBusy            => bAxisVirtual_RelBusy,
    AxisError          => bAxisVirtual_AxisError,
    AxisAccing         => bAxisVirtual_Accing,
    AxisDecing         => bAxisVirtual_Decing,
    FBErrorOccurred    => ,                        (* 图中未连接，留空 *)
    Homing             => ,                        (* 图中未连接，留空 *)
    Stopping           => ,                        (* 图中未连接，留空 *)
    ErrorID            => ,                        (* 图中未连接，留空 *)
    SetPosDone         => ,                        (* 图中未连接，留空 *)
    bOperational       => ,                        (* 图中未连接，留空 *)
	eComState          => ,
    wComState          => ,                        (* 图中未连接，留空 *)
    JogBusy            => bAxisVirtual_JogBusy      (* JogBusy 连线到 bAxisVirtual_JogBusy *)
	ReStartSlaveDone   =>
);

FB_AxisStop_AxisVirtual(
	StopExcute := bAxisVirtual_StopExcute
);

SMC_ClearFBError(
	EN := FBErrorOccured,
	pDrive := ADR(AxisVirtual),
	ENO => ,
	SMC_ClearFBError =>
);

SMC_ChangeGearingRatio0(
    (* =============== 输入参数 ( := ) =============== *)
    Axis                 := AxisVirtual,
    bExecute             := ,                            (* FBD中 bExecute 引脚未连接，留空 *)
    dwRatioTechUnitsDenom:= AxisVirtual.dwRatioTechUnitsDenom, (* 分母：连接到轴变量的 Denom *)
    iRatioTechUnitsNum   := REAL_TO_INT(HMI_rAxisVirtual_Lead), (* 分子：HMI输入的REAL转INT后连接 *)
    fPositionPeriod      := ,                            (* FBD中 fPositionPeriod 未连接，留空 *)
    iMovementType        := SMC_MOVEMENTTYPE.linear,      (* 运动类型常量连接 *)

    (* =============== 输出参数 ( => ) =============== *)
    bDone                => ,
    bBusy                => ,
    bError               => ,
    nErrorID             => 
);


AxisVirtual.iRestNumerator = 0;
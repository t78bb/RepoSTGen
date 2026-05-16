(*基本速度，位置*)
rAxisVirtual_JogVelSet:=HMI_rAxisVirtual_ManualVel;

rAxisVirtual_AbsVelSet:=HMI_rAxisVirtual_AutoVel;
rAxisVirtual_RelVelSet:=HMI_rAxisVirtual_AutoVel;
rAxisVirtual_VelVelSet:=HMI_rAxisVirtual_AutoVel;
rAxisVirtual_InchVelSet:=HMI_rAxisVirtual_AutoVel;

HMI_rAxisVirtual_ActPos:=LREAL_TO_REAL(AxisVirtual.fActPosition);
HMI_rAxisVirtual_ActVel:=LREAL_TO_REAL(AxisVirtual.fActVelocity);

FB_AxisControl_AxisVirtual.AbsAcceleration:=rAxisVirtual_AbsVelSet*10000;
FB_AxisControl_AxisVirtual.AbsDeceleration:=rAxisVirtual_AbsVelSet*10000;

FB_AxisControl_AxisVirtual.RelAcceleration:=rAxisVirtual_RelVelSet*10000;
FB_AxisControl_AxisVirtual.RelDeceleration:=rAxisVirtual_RelVelSet*10000;

FB_AxisControl_AxisVirtual.InchAcceleration:=rAxisVirtual_InchVelSet*10000;
FB_AxisControl_AxisVirtual.InchDeceleration:=rAxisVirtual_InchVelSet*10000;

(*正负限位*)
IF bAxisVirtual_LimitEnable AND bAxisVirtual_HomeDone THEN
	AxisVirtual.bSWLimitEnable:=TRUE;
	AxisVirtual.fSWLimitPositive:=HMI_rAxisVirtual_LimitPostive;
	AxisVirtual.fSWLimitNegative:=HMI_rAxisVirtual_LimitNegative;
	AxisVirtual.fSWLimitDeceleration:=1000000;
	ELSE
	AxisVirtual.bSWLimitEnable:=FALSE;	
END_IF


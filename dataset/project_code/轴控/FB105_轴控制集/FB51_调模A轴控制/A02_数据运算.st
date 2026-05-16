(*基本速度，位置*)
r调模A轴点动速度给定:=HMI_r调模A轴手动速度;

r调模A轴绝对运动速度给定:=HMI_r调模A轴自动速度;
r调模A轴相对运动速度给定:=HMI_r调模A轴自动速度;
r调模A轴速度模式速度给定:=HMI_r调模A轴自动速度;
r调模A轴寸动速度给定:=HMI_r调模A轴自动速度;

HMI_r调模A轴当前位置:=LREAL_TO_REAL(AxisLeftTiaoMo.fActPosition);
HMI_r调模A轴当前速度:=LREAL_TO_REAL(AxisLeftTiaoMo.fActVelocity);

FB_AxisControl_调模A轴.AbsAcceleration:=r调模A轴绝对运动速度给定/(HMI_r调模A轴加速时间/1000);
FB_AxisControl_调模A轴.AbsDeceleration:=r调模A轴绝对运动速度给定/(HMI_r调模A轴减速时间/1000);

FB_AxisControl_调模A轴.RelAcceleration:=r调模A轴相对运动速度给定/(HMI_r调模A轴加速时间/1000);
FB_AxisControl_调模A轴.RelDeceleration:=r调模A轴相对运动速度给定/(HMI_r调模A轴减速时间/1000);

FB_AxisControl_调模A轴.InchAcceleration:=r调模A轴寸动速度给定/(HMI_r调模A轴加速时间/1000);
FB_AxisControl_调模A轴.InchDeceleration:=r调模A轴寸动速度给定/(HMI_r调模A轴减速时间/1000);

(*正负限位*)
IF b调模A轴启用限位 AND b调模A轴回零完成 THEN
	AxisLeftTiaoMo.bSWLimitEnable:=TRUE;
	AxisLeftTiaoMo.fSWLimitPositive:=HMI_r调模A轴正限位;
	AxisLeftTiaoMo.fSWLimitNegative:=HMI_r调模A轴负限位;
	AxisLeftTiaoMo.fSWLimitDeceleration:=1000000;
	ELSE
	AxisLeftTiaoMo.bSWLimitEnable:=FALSE;	
END_IF


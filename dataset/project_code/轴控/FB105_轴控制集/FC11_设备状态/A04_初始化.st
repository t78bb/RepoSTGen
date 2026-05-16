TON0(IN:= HMI_b初始化, PT:= T#3S, Q=> , ET=> );
TON1(IN:= HMI_b初始化, PT:= T#2S, Q=> , ET=> );
R_TRIG0(CLK:= TON0.Q AND b所有伺服使能OK AND b所有伺服总线通讯OK AND NOT b设备报警 AND b非急停手动模式 AND NOT b设备初始化中, Q=> );
R_TRIG1(CLK:= TON1.Q AND b所有伺服使能OK AND b所有伺服总线通讯OK AND NOT b设备报警 AND b非急停手动模式 AND NOT b设备初始化中, Q=> );

IF R_TRIG1.Q THEN
	b轴控初始化:=TRUE;
END_IF
TON4(IN:= b轴控初始化, PT:= T#0.3S, Q=> , ET=> );
IF TON4.Q THEN
	b轴控初始化:=FALSE;
END_IF

IF NOT DI_急停按钮 THEN
	i初始化步:=0;
	b设备初始化中:=FALSE;
	b调模A轴回零触发:=FALSE;
	b调模B轴回零触发:=FALSE;
	b送面料轴回零触发:=FALSE;
	b取面料轴回零触发:=FALSE;
	b横移A轴回零触发:=FALSE;
	b升降A轴回零触发:=FALSE;
	b横移B轴回零触发:=FALSE;
	b升降B轴回零触发:=FALSE;
	b出盒轴回零触发:=FALSE;
	b铲灰板轴回零触发:=FALSE;
	b包面纸轴回零触发:=FALSE;
	b上包底轴回零触发:=FALSE;
	b折边轴回零触发:=FALSE;
END_IF


CASE i初始化步 OF
	0:
	IF R_TRIG0.Q THEN
		b设备初始化中:=TRUE;
		i初始化步:=1;
	END_IF
	
	1:
	IF b设备初始化中 THEN
		b自动运行:=FALSE; b自动互锁:=FALSE;
		TON2(IN:= TRUE, PT:= T#0.2S, Q=> , ET=> );
		IF TON2.Q THEN
			TON2(IN:= FALSE,  );
			i初始化步:=5;
		END_IF
		
	END_IF
	
	5:
	
	IF b设备初始化中 THEN
		DO_取料气缸:=FALSE; DO_纠偏气缸:=FALSE; DO_挡料定位气缸:=FALSE; DO_翻板气缸:=FALSE; DO_侧压紧气缸:=FALSE;
		DO_左A包底气缸:=FALSE; DO_右B包底气缸:=FALSE; DO_上包底气缸:=FALSE; DO_下包底气缸:=FALSE; DO_出料推盒气缸:=FALSE;
		DO_包盒口升降气缸:=FALSE; DO_包盒口下压气缸:=FALSE; DO_翻底板气缸:=FALSE; DO_推底板气缸:=FALSE; DO_模组吸底板气缸:=FALSE;
		DO_包边纠偏上下气缸:=FALSE; DO_包边纠偏左右气缸:=FALSE; DO_包边压料气缸:=FALSE; DO_折边上托气缸:=FALSE; 
        DO_包边铲边气缸:=FALSE; DO_吸底板真空:=FALSE; DO_取面板真空:=FALSE; DO_A模吸底板真空:=FALSE; DO_A模吸面板真空:=FALSE;
		DO_B模吸底板真空:=FALSE; DO_B模吸面板真空:=FALSE; DO_真空泵:=FALSE; DO_出料皮带电机:=FALSE; 
		IF b所有气缸原位OK AND b所有气缸关闭OK THEN 
			i初始化步:=10;
		END_IF
	END_IF
	
	10:
	IF b设备初始化中 THEN
		b调模A轴回零触发:=TRUE;
		b调模B轴回零触发:=TRUE;
		b送面料轴回零触发:=TRUE;
		b取面料轴回零触发:=TRUE;
		b横移A轴回零触发:=TRUE;
		b升降A轴回零触发:=TRUE;
		b横移B轴回零触发:=TRUE;
		b升降B轴回零触发:=TRUE;
		b出盒轴回零触发:=TRUE;
		b铲灰板轴回零触发:=TRUE;
		b包面纸轴回零触发:=TRUE;
		b上包底轴回零触发:=TRUE;
		b折边轴回零触发:=TRUE;
		TON3(IN:= TRUE, PT:= T#0.2S, Q=> , ET=> );
		IF TON3.Q AND b所有伺服静止中 THEN
			b调模A轴回零触发:=FALSE;
		    b调模B轴回零触发:=FALSE;
		    b送面料轴回零触发:=FALSE;
		    b取面料轴回零触发:=FALSE;
		    b横移A轴回零触发:=FALSE;
		    b升降A轴回零触发:=FALSE;
		    b横移B轴回零触发:=FALSE;
		    b升降B轴回零触发:=FALSE;
		    b出盒轴回零触发:=FALSE;
		    b铲灰板轴回零触发:=FALSE;
		    b包面纸轴回零触发:=FALSE;
		    b上包底轴回零触发:=FALSE;
		    b折边轴回零触发:=FALSE;
			TON3(IN:= FALSE,  );
			i初始化步:=15;
		END_IF
 
	END_IF
	
	15:
	IF b设备初始化中 THEN
		b设备初始化中:=FALSE;
		i初始化步:=0;
	END_IF
END_CASE

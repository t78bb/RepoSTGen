(**************************************************底膜部分*************************************************)
R_TRIG手动[1](CLK:= HMI_b取料气缸, Q=> );          F_TRIG手动[1](CLK:= HMI_b取料气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[1].Q THEN
    DO_取料气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[1].Q THEN
    DO_取料气缸:=FALSE;
END_IF

R_TRIG手动[2](CLK:= HMI_b纠偏气缸, Q=> );          F_TRIG手动[2](CLK:= HMI_b纠偏气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[2].Q THEN
    DO_纠偏气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[2].Q THEN
    DO_纠偏气缸:=FALSE;
END_IF

R_TRIG手动[3](CLK:= HMI_b挡料定位气缸, Q=> );      F_TRIG手动[3](CLK:= HMI_b挡料定位气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[3].Q THEN
    DO_挡料定位气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[3].Q THEN
    DO_挡料定位气缸:=FALSE;
END_IF

R_TRIG手动[4](CLK:= HMI_b翻板气缸, Q=> );          F_TRIG手动[4](CLK:= HMI_b翻板气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[4].Q THEN
    DO_翻板气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[4].Q THEN
    DO_翻板气缸:=FALSE;
END_IF

R_TRIG手动[5](CLK:= HMI_b侧压紧气缸, Q=> );         F_TRIG手动[5](CLK:= HMI_b侧压紧气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[5].Q THEN
    DO_侧压紧气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[5].Q THEN
    DO_侧压紧气缸:=FALSE;
END_IF

R_TRIG手动[6](CLK:= HMI_b左A包底气缸, Q=> );        F_TRIG手动[6](CLK:= HMI_b左A包底气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[6].Q THEN
    DO_左A包底气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[6].Q THEN
    DO_左A包底气缸:=FALSE;
END_IF

R_TRIG手动[7](CLK:= HMI_b右B包底气缸, Q=> );        F_TRIG手动[7](CLK:= HMI_b右B包底气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[7].Q THEN
    DO_右B包底气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[7].Q THEN
    DO_右B包底气缸:=FALSE;
END_IF

R_TRIG手动[8](CLK:= HMI_b上包底气缸, Q=> );         F_TRIG手动[8](CLK:= HMI_b上包底气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[8].Q THEN
    DO_上包底气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[8].Q THEN
    DO_上包底气缸:=FALSE;
END_IF

R_TRIG手动[9](CLK:= HMI_b下包底气缸, Q=> );         F_TRIG手动[9](CLK:= HMI_b下包底气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[9].Q THEN
    DO_下包底气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[9].Q THEN
    DO_下包底气缸:=FALSE;
END_IF

R_TRIG手动[10](CLK:= HMI_b出料推盒气缸, Q=> );      F_TRIG手动[10](CLK:= HMI_b出料推盒气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[10].Q THEN
    DO_出料推盒气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[10].Q THEN
    DO_出料推盒气缸:=FALSE;
END_IF

R_TRIG手动[11](CLK:= HMI_b包盒口升降气缸, Q=> );    F_TRIG手动[11](CLK:= HMI_b包盒口升降气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[11].Q THEN
    DO_包盒口升降气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[11].Q THEN
    DO_包盒口升降气缸:=FALSE;
END_IF

R_TRIG手动[12](CLK:= HMI_b包盒口下压气缸, Q=> );    F_TRIG手动[12](CLK:= HMI_b包盒口下压气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[12].Q THEN
    DO_包盒口下压气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[12].Q THEN
    DO_包盒口下压气缸:=FALSE;
END_IF

R_TRIG手动[13](CLK:= HMI_b翻底板气缸, Q=> );        F_TRIG手动[13](CLK:= HMI_b翻底板气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[13].Q THEN
    DO_翻底板气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[13].Q THEN
    DO_翻底板气缸:=FALSE;
END_IF

R_TRIG手动[14](CLK:= HMI_b推底板气缸, Q=> );        F_TRIG手动[14](CLK:= HMI_b推底板气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[14].Q THEN
    DO_推底板气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[14].Q THEN
    DO_推底板气缸:=FALSE;
END_IF

R_TRIG手动[15](CLK:= HMI_b模组吸底板气缸, Q=> );    F_TRIG手动[15](CLK:= HMI_b模组吸底板气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[15].Q THEN
    DO_模组吸底板气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[15].Q THEN
    DO_模组吸底板气缸:=FALSE;
END_IF

R_TRIG手动[16](CLK:= HMI_b包边纠偏上下气缸, Q=> );  F_TRIG手动[16](CLK:= HMI_b包边纠偏上下气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[16].Q THEN
    DO_包边纠偏上下气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[16].Q THEN
    DO_包边纠偏上下气缸:=FALSE;
END_IF

R_TRIG手动[17](CLK:= HMI_b包边纠偏左右气缸, Q=> );  F_TRIG手动[17](CLK:= HMI_b包边纠偏左右气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[17].Q THEN
    DO_包边纠偏左右气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[17].Q THEN
    DO_包边纠偏左右气缸:=FALSE;
END_IF

R_TRIG手动[18](CLK:= HMI_b包边压料气缸, Q=> );      F_TRIG手动[18](CLK:= HMI_b包边压料气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[18].Q THEN
    DO_包边压料气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[18].Q THEN
    DO_包边压料气缸:=FALSE;
END_IF

R_TRIG手动[19](CLK:= HMI_b折边上托气缸, Q=> );      F_TRIG手动[19](CLK:= HMI_b折边上托气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[19].Q THEN
    DO_折边上托气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[19].Q THEN
    DO_折边上托气缸:=FALSE;
END_IF

R_TRIG手动[20](CLK:= HMI_b包边铲边气缸, Q=> );      F_TRIG手动[20](CLK:= HMI_b包边铲边气缸, Q=> );
IF b非急停手动模式 AND R_TRIG手动[20].Q THEN
    DO_包边铲边气缸:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[20].Q THEN
    DO_包边铲边气缸:=FALSE;
END_IF
(**************************************************其它部分*************************************************)
R_TRIG手动[80](CLK:= HMI_b真空泵, Q=> );        F_TRIG手动[80](CLK:= HMI_b真空泵, Q=> );
IF b非急停手动模式 AND R_TRIG手动[80].Q THEN
    DO_真空泵:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[80].Q THEN
    DO_真空泵:=FALSE;
END_IF

R_TRIG手动[81](CLK:= HMI_b出料皮带电机, Q=> );   F_TRIG手动[81](CLK:= HMI_b出料皮带电机, Q=> );
IF b非急停手动模式 AND R_TRIG手动[81].Q THEN
    DO_出料皮带电机:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[81].Q THEN
    DO_出料皮带电机:=FALSE;
END_IF
(**************************************************真空部分*************************************************)
R_TRIG手动[50](CLK:= HMI_b吸底板真空, Q=> );   F_TRIG手动[50](CLK:= HMI_b吸底板真空, Q=> );
IF b非急停手动模式 AND R_TRIG手动[50].Q THEN
    DO_吸底板真空:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[50].Q THEN
    DO_吸底板真空:=FALSE;
END_IF

R_TRIG手动[51](CLK:= HMI_b取面板真空, Q=> );   F_TRIG手动[51](CLK:= HMI_b取面板真空, Q=> );
IF b非急停手动模式 AND R_TRIG手动[51].Q THEN
    DO_取面板真空:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[51].Q THEN
    DO_取面板真空:=FALSE;
END_IF

R_TRIG手动[52](CLK:= HMI_bA模吸底板真空, Q=> );   F_TRIG手动[52](CLK:= HMI_bA模吸底板真空, Q=> );
IF b非急停手动模式 AND R_TRIG手动[52].Q THEN
    DO_A模吸底板真空:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[52].Q THEN
    DO_A模吸底板真空:=FALSE;
END_IF

R_TRIG手动[53](CLK:= HMI_bA模吸面板真空, Q=> );   F_TRIG手动[53](CLK:= HMI_bA模吸面板真空, Q=> );
IF b非急停手动模式 AND R_TRIG手动[53].Q THEN
    DO_A模吸面板真空:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[53].Q THEN
	DO_A模吸面板真空:=FALSE;
END_IF

R_TRIG手动[54](CLK:= HMI_bB模吸底板真空, Q=> );   F_TRIG手动[54](CLK:= HMI_bB模吸底板真空, Q=> );
IF b非急停手动模式 AND R_TRIG手动[54].Q THEN
    DO_B模吸底板真空:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[54].Q THEN
    DO_B模吸底板真空:=FALSE;
END_IF

R_TRIG手动[55](CLK:= HMI_bB模吸面板真空, Q=> );   F_TRIG手动[55](CLK:= HMI_bB模吸面板真空, Q=> );
IF b非急停手动模式 AND R_TRIG手动[55].Q THEN
    DO_B模吸面板真空:=TRUE;
END_IF
IF b非急停手动模式 AND F_TRIG手动[55].Q THEN
	DO_B模吸面板真空:=FALSE;
END_IF





FUNCTION_BLOCK FB_卷径计算
VAR_INPUT
   En  :BOOL;  (*使能功能块*)
   xMode :BOOL; (*FALSE*) 
   xSet :BOOL;  (*初始化卷径*)
   Dir     :BOOL;   (*倒纸*)
   AxisDir :BOOL;  (*轴换向*)
   rDiaInit :REAL; (*初始卷径*)
   rDiaMax:REAL; (*最大卷径*)
   Length :REAL; (*采样长度*)
   rRatio :REAL; (*齿轮比，1.0*)
   MasterPos :LREAL; (*主轴当前位置*)
   SlavePos :LREAL;  (*从轴当前位置*)

END_VAR
VAR_OUTPUT
 RampDia:REAL;   (*斜坡后的可显示卷径*)
END_VAR
VAR
 fbR_TRIG: R_TRIG;
 rOldMasterPos:LREAL;
 rOldSlavePos:LREAL;
 rMasterLength:REAL;
 rSlaveLength:REAL;
 RAMP_REAL1: RAMP_REAL;
END_VAR
VAR_IN_OUT
 Diameter: REAL;  (*实时卷径*)
END_VAR

fbR_TRIG(CLK:=En , Q=> );
IF fbR_TRIG.Q THEN
    rOldMasterPos:=MasterPos;
    rOldSlavePos:=SlavePos;
END_IF

IF xSet THEN
    Diameter:=rDiaInit;
END_IF
 
IF NOT AxisDir AND NOT Dir AND En THEN
    IF SlavePos>rOldSlavePos+Length*rRatio THEN
        rMasterLength:=MasterPos-rOldMasterPos;
        rSlaveLength:=MasterPos-rOldSlavePos;
        Diameter:=rMasterLength/(3.14*rRatio);
        rOldMasterPos:=MasterPos;
        rOldSlavePos:=SlavePos;
    END_IF
END_IF
IF AxisDir AND NOT Dir AND En THEN
    IF SlavePos<rOldSlavePos-Length*rRatio THEN
        rMasterLength:=MasterPos-rOldMasterPos;
        rSlaveLength:=MasterPos-rOldSlavePos;
        Diameter:=rMasterLength/(3.14*rRatio);
        rOldMasterPos:=MasterPos;
        rOldSlavePos:=SlavePos;
    END_IF
END_IF

IF NOT AxisDir AND Dir AND En THEN
    IF SlavePos<rOldSlavePos-Length*rRatio THEN
        rMasterLength:=MasterPos-rOldMasterPos;
        rSlaveLength:=MasterPos-rOldSlavePos;
        Diameter:=rMasterLength/(3.14*rRatio);
        rOldMasterPos:=MasterPos;
        rOldSlavePos:=SlavePos;
    END_IF
END_IF
IF AxisDir AND Dir AND En THEN
    IF SlavePos>rOldSlavePos+Length*rRatio THEN
        rMasterLength:=MasterPos-rOldMasterPos;
        rSlaveLength:=MasterPos-rOldSlavePos;
        Diameter:=rMasterLength/(3.14*rRatio);
        rOldMasterPos:=MasterPos;
        rOldSlavePos:=SlavePos;
    END_IF
END_IF

RAMP_REAL1(
	IN:= , 
	ASCEND:= , 
	DESCEND:= , 
	TIMEBASE:= T#10MS, 
	RESET:= , 
	OUT=> RampDia);
	
IF NOT xMode THEN
    RAMP_REAL1.ASCEND:=0.01;
    RAMP_REAL1.DESCEND:=0.005;
END_IF

IF xMode THEN
    RAMP_REAL1.ASCEND:=0.005;
    RAMP_REAL1.DESCEND:=0.01;
END_IF

IF xSet THEN
    RAMP_REAL1.ASCEND:=400;
    RAMP_REAL1.DESCEND:=400;
END_IF
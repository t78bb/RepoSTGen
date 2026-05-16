PROGRAM JOG
VAR
	fbJogM	:	SM3_Basic.MC_Jog;
	fbJogS	:	SM3_Basic.MC_Jog;
END_VAR

fbJogM(Axis:=AxisM,JogForward:=MHmiJogMP,JogBackward:=MHmiJogMN,Velocity:=MHmiInJogVel,Acceleration:=3600,Deceleration:=3600);
fbJogS(Axis:=AxisS,JogForward:=MHmiJogSN,JogBackward:=MHmiJogSP,Velocity:=MHmiInJogVel,Acceleration:=3600,Deceleration:=3600);
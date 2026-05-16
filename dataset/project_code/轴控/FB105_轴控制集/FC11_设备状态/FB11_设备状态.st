PROGRAM FC11_设备状态
VAR
	fb_bFristScan: TON;


	TON0: TON;
	TON1: TON;
	TON2: TON;
	TON3: TON;
	TON4: TON;
	
	i初始化步: INT;
	
	R_TRIG0: R_TRIG;
	R_TRIG1: R_TRIG;

END_VAR


(*IO功能启用*)
//NET_IO_Cmd(SysWarnID:= , bError=> , nErrorID=> );

(*子程序调用*)
A01_输入映射();

A02_输出映射();

A03_气缸状态();

A04_初始化();

(*开机初始化*)
fb_bFristScan(IN:= b常闭, PT:= T#1S, Q=> , ET=> );
IF TIME_TO_REAL(fb_bFristScan.ET)>500 AND TIME_TO_REAL(fb_bFristScan.ET)<600 THEN
	b开机初始化:=TRUE;
	ELSE
	b开机初始化:=FALSE;	
END_IF

IF NOT b常通 THEN
	b开机第一次启动:=TRUE;
	ELSE
	b开机第一次启动:=FALSE;	
END_IF
IF b开机第一次启动 OR b常通 THEN
	b常通:=TRUE;
	ELSE
	b常通:=FALSE;	
END_IF
(*
IF EtherCAT_Master_Leadshine.xConfigFinished AND EtherCAT_Master_Leadshine.xDistributedClockInSync AND 
   NOT EtherCAT_Master_Leadshine.xError AND NOT b常闭 THEN
	b开机初始化:=TRUE;
	ELSE
	b开机初始化:=FALSE;	
END_IF   
*)   

(*状态判定*)
IF DI_急停按钮 AND NOT HMI_b手动模式0自动模式1 THEN
	b非急停手动模式:=TRUE;
	ELSE
	b非急停手动模式:=FALSE;	
END_IF
IF DI_急停按钮 AND HMI_b手动模式0自动模式1 THEN
	b非急停自动模式:=TRUE;
	ELSE
	b非急停自动模式:=FALSE;	
END_IF




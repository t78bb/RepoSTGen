PROGRAM FC10_设备轴类
VAR
	pSlave: POINTER TO ETCSlave;
    No_Slave: INT;	
	bEtcReset: BOOL;
	
END_VAR

VAR_OUTPUT
	ERROR: ARRAY[1..13] OF INT;
END_VAR

A01_通讯状态();
A02_各轴状态();

FB50_虚轴控制();
FB51_调模A轴控制();
FB52_调模B轴控制();
FB53_送面料轴控制();
FB54_取面料轴控制();
FB55_横移A轴控制();
FB56_升降A轴控制();
FB57_横移B轴控制();
FB58_升降B轴控制();
FB59_出盒轴控制();
FB60_铲灰板轴控制();
FB61_包面纸轴控制();
FB62_上包底轴控制();
FB63_折边轴控制();



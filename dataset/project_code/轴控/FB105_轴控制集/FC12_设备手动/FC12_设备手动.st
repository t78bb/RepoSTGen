PROGRAM FC12_设备手动
VAR
	R_TRIG手动: ARRAY[1..100] OF R_TRIG;
	F_TRIG手动: ARRAY[1..100] OF F_TRIG;
END_VAR

A01_气类操作();
A02_轴类手动();
A03_气缸手动();
A04_真空手动();
A05_其它手动();
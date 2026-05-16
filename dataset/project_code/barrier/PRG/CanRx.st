PROGRAM CanRx
VAR
	count		:UINT;
END_VAR

count := count + 1;
IF count > 1000 THEN
	count := 1;
END_IF

C01_Rx();
C02_Rx();
C03_Rx();
C04_Rx();
C05_Rx();
C06_Rx();


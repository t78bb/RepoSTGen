PROGRAM CanTx
VAR
	count		:UINT;
END_VAR

count := count + 1;
IF count > 1000 THEN
	count := 1;
END_IF

C01_Tx();
C02_Tx();
C03_Tx();
C04_Tx();
C05_Tx();
C06_Tx();